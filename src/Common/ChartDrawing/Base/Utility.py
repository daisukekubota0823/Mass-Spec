import math
from typing import List, Tuple, Optional
from collections import defaultdict

# Placeholder classes
class DrawVisual:
    def __init__(self, area=None, title=None, series_list=None):
        self.MinX = float('-inf')
        self.MaxX = float('inf')
        self.MinY = float('-inf')
        self.MaxY = float('inf')
        self.SeriesList = series_list

class Area:
    def __init__(self, axis_x=None, axis_y=None, margin=None):
        self.AxisX = axis_x
        self.AxisY = axis_y
        self.Margin = margin

class AxisX:
    def __init__(self, axis_label="", pen=None, font_size=12):
        self.AxisLabel = axis_label
        self.Pen = pen
        self.FontSize = font_size

class AxisY:
    def __init__(self, axis_label="", pen=None, font_size=12):
        self.AxisLabel = axis_label
        self.Pen = pen
        self.FontSize = font_size

class SeriesList:
    def __init__(self):
        self.Series = []
        self.MinX = 0
        self.MaxX = 0
        self.MinY = 0
        self.MaxY = 0

class Series:
    def __init__(self, chart_type="Line", marker_type="None", brush=None, pen=None, marker_size=(2, 2)):
        self.ChartType = chart_type
        self.MarkerType = marker_type
        self.Brush = brush
        self.Pen = pen
        self.MarkerSize = marker_size
        self.Points = []
        self.Legend = None

    def AddPoint(self, x, y):
        self.Points.append((x, y))

class Legend:
    def __init__(self, text="", is_visible=True):
        self.Text = text
        self.IsVisible = is_visible

class XY:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

class DirectedTree:
    def __init__(self):
        self.Count = 0
        self.Leaves = []
        self.Root = 0

    def PostOrder(self, root, func):
        pass

    def PreOrder(self, root, func):
        pass


class Utility:
    @staticmethod
    def SetDrawingMinAndMaxXYConstValue(drawing: DrawVisual, min_x=float('-inf'), max_x=float('inf'), min_y=float('-inf'), max_y=float('inf')):
        if min_x > float('-inf'):
            drawing.MinX = min_x
        if max_x > float('-inf'):
            drawing.MaxX = max_x
        if min_y > float('-inf'):
            drawing.MinY = min_y
        if max_y > float('-inf'):
            drawing.MaxY = max_y

    @staticmethod
    def SetDrawingMinXRatio(drawing: DrawVisual, ratio: float):
        drawing.MinX -= (drawing.SeriesList.MaxX - drawing.SeriesList.MinX) * ratio

    @staticmethod
    def SetDrawingMinYRatio(drawing: DrawVisual, ratio: float):
        drawing.MinY -= (drawing.SeriesList.MaxY - drawing.SeriesList.MinY) * ratio

    @staticmethod
    def SetDrawingMaxXRatio(drawing: DrawVisual, ratio: float):
        drawing.MaxX += (drawing.SeriesList.MaxX - drawing.SeriesList.MinX) * ratio

    @staticmethod
    def SetDrawingMaxYRatio(drawing: DrawVisual, ratio: float):
        drawing.MaxY += (drawing.SeriesList.MaxY - drawing.SeriesList.MinY) * ratio

    @staticmethod
    def GetDefaultAreaV1(xlabel="Retention time (min)", ylabel="RT diff (Sample - Reference) (sec)"):
        area = Area(
            axis_x=AxisX(axis_label=xlabel, pen="Black", font_size=12),
            axis_y=AxisY(axis_label=ylabel, pen="Black", font_size=12)
        )
        return area

    @staticmethod
    def GetDefaultAreaV2(xlabel="Retention time (min)"):
        area = Area(
            axis_x=AxisX(axis_label=xlabel, pen="DarkGray", font_size=12),
            axis_y=AxisY(axis_label="", pen="DarkGray", font_size=12),
            margin=(20, 30, 10, 40)
        )
        return area

    @staticmethod
    def GetDefaultTitleV1(fontsize=13, label="Overview: Retention time correction"):
        return {"FontSize": fontsize, "Label": label}

    @staticmethod
    def GetLineChartV1SeriesList(target_list_list: List[List[Tuple[float, float]]], brushes: Optional[List[str]] = None):
        slist = SeriesList()
        for i, target_list in enumerate(target_list_list):
            brush = "Blue" if brushes is None or brushes[i] is None else brushes[i]
            series = Series(chart_type="Line", marker_type="None", brush=brush, pen=brush)
            for value in target_list:
                series.AddPoint(value[0], value[1])
            if series.Points:
                slist.Series.append(series)
        return slist

    @staticmethod
    def GetLineChartV1(target_list_list: List[List[Tuple[float, float]]]):
        area = Utility.GetDefaultAreaV1()
        title = Utility.GetDefaultTitleV1()
        slist = Utility.GetLineChartV1SeriesList(target_list_list)
        return DrawVisual(area, title, slist)

    @staticmethod
    def CombineAlphaAndColor(opacity: float, base_color: Tuple[int, int, int]):
        r, g, b = base_color
        a = max(0, min(255, int(255 * opacity)))
        return (a, r, g, b)

    @staticmethod
    def RoundUp(value: float, digits: int):
        coef = 10 ** digits
        return math.ceil(value * coef) / coef

    @staticmethod
    def RoundDown(value: float, digits: int):
        coef = 10 ** digits
        return math.floor(value * coef) / coef

    @staticmethod
    def CalculateTreeCoordinate(tree: DirectedTree):
        if tree.Count == 0:
            return []
        xys = [XY() for _ in range(tree.Count)]
        root = tree.Root

        def post_order_action(e):
            xys[e.To].X = tree[e.To].Count() == 0 and counter or sum(xys[e_.To].X for e_ in tree[e.To]) / len(tree[e.To])

        counter = 0
        tree.PostOrder(root, post_order_action)

        def pre_order_action(e):
            xys[e.To].Y = xys[e.From].Y + e.Distance

        tree.PreOrder(root, pre_order_action)
        ymax = max(xy.Y for xy in xys)
        for xy in xys:
            xy.Y = ymax - xy.Y
        return xys
