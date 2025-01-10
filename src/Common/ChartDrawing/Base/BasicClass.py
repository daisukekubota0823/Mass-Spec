from enum import Enum
from typing import List, Optional, Iterator


class ChartType(Enum):
    Line = "Line"
    Point = "Point"
    Chromatogram = "Chromatogram"
    MS = "MS"
    MSwithRef = "MSwithRef"


class MarkerType(Enum):
    NoneType = "None"
    Circle = "Circle"
    Square = "Square"
    Cross = "Cross"


class XaxisUnit(Enum):
    Minutes = "Minutes"
    Seconds = "Seconds"


class Position(Enum):
    Left = "Left"
    Right = "Right"
    Top = "Top"
    Bottom = "Bottom"


class MouseActionSetting:
    def __init__(self):
        self.can_mouse_action = True
        self.can_zoom_rubber = True
        self.fix_min_x = False
        self.fix_max_x = False
        self.fix_min_y = False
        self.fix_max_y = False


class Margin:
    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class LabelSpace(Margin):
    pass


class Axis:
    def __init__(self):
        self.axis_label = ""
        self.minor_scale_size = 2
        self.major_scale_size = 5
        self.font_type = "Calibri"
        self.font_size = 13
        self.font_color = "Black"
        self.pen = "Black"
        self.enabled = True
        self.scale_enabled = True
        self.minor_scale_enabled = True
        self.is_italic_label = False


class AxisX(Axis):
    def __init__(self):
        super().__init__()
        self.axis_label = "X axis"


class AxisY(Axis):
    def __init__(self):
        super().__init__()
        self.axis_label = "Y axis"


class Area:
    def __init__(self):
        self.axis_x = AxisX()
        self.axis_y = AxisY()
        self.margin = Margin(60, 30, 10, 40)
        self.label_space = LabelSpace(0, 0, 0, 0)
        self.height = 0.0
        self.width = 0.0
        self.background_color = "WhiteSmoke"
        self.graph_border = "LightGray"

    @property
    def actual_graph_height(self):
        return self.height - self.margin.top - self.margin.bottom

    @property
    def actual_graph_width(self):
        return self.width - self.margin.left - self.margin.right


class Title:
    def __init__(self):
        self.label = ""
        self.font_type = "Calibri"
        self.font_size = 12
        self.font_color = "Black"
        self.fit_font_size = False
        self.enabled = True


class Legend:
    def __init__(self):
        self.text = ""
        self.is_visible = False
        self.position = Position.Right
        self.in_graphic_area = True
        self.max_width = 100
        self.font_size = 13


class XY:
    def __init__(self, x=0.0, y=0.0, label=""):
        self.x = x
        self.y = y
        self.label = label


class Series:
    def __init__(self):
        self.points: List[XY] = []
        self.legend = None
        self.is_label_visible = False
        self.chart_type = ChartType.Line
        self.marker_type = MarkerType.NoneType
        self.xaxis_unit = XaxisUnit.Minutes
        self.marker_size = (2, 2)
        self.marker_fill = "Red"
        self.brush = "Black"
        self.pen = "Black"
        self.font_type = "Calibri"
        self.font_size = 13
        self.accessory = None

    @property
    def max_x(self) -> float:
        return max((point.x for point in self.points), default=0.0)

    @property
    def min_x(self) -> float:
        return min((point.x for point in self.points), default=0.0)

    @property
    def max_y(self) -> float:
        return max((point.y for point in self.points), default=0.0)

    @property
    def min_y(self) -> float:
        return min((point.y for point in self.points), default=0.0)

    def add_point(self, x=0.0, y=0.0, label=""):
        self.points.append(XY(x, y, label))


class Accessory:
    class PeakInfo:
        def __init__(self):
            self.rt_top = -1.0
            self.rt_left = -1.0
            self.rt_right = -1.0
            self.area_factor = 1.0
            self.signal_to_noise = 1.0
            self.estimated_noise = 1.0

    def __init__(self):
        self.chromatogram = Accessory.PeakInfo()

    def set_chromatogram(self, rt_top, rt_left, rt_right, estimated_noise=1.0, signal_to_noise=1.0, area_factor=1.0):
        width = rt_right - rt_left
        if width < 0.00001:
            self.chromatogram = Accessory.PeakInfo()
        else:
            self.chromatogram = Accessory.PeakInfo()
            self.chromatogram.rt_top = rt_top
            self.chromatogram.rt_left = rt_left
            self.chromatogram.rt_right = rt_right
            self.chromatogram.area_factor = area_factor
            self.chromatogram.signal_to_noise = signal_to_noise
            self.chromatogram.estimated_noise = estimated_noise


class SeriesList:
    def __init__(self):
        self.series_list: List[Series] = []

    @property
    def max_x(self) -> float:
        return max((series.max_x for series in self.series_list), default=float("-inf"))

    @property
    def min_x(self) -> float:
        return min((series.min_x for series in self.series_list), default=float("inf"))

    @property
    def max_y(self) -> float:
        return max((series.max_y for series in self.series_list), default=float("-inf"))

    @property
    def min_y(self) -> float:
        return min((series.min_y for series in self.series_list), default=float("inf"))

    def add_series(self, series: Series):
        self.series_list.append(series)

    def __iter__(self) -> Iterator[Series]:
        return iter(self.series_list)
