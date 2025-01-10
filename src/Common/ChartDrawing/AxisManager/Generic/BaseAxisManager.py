from typing import List, TypeVar, Generic, Callable, Optional, Union
from abc import ABC, abstractmethod
import math

T = TypeVar('T')

class AxisValue:
    def __init__(self, value: float):
        self.value = value

    @property
    def Value(self):
        return self.value


class AxisRange:
    def __init__(self, minimum: AxisValue, maximum: AxisValue):
        self.Minimum = minimum
        self.Maximum = maximum

    @property
    def Delta(self):
        return self.Maximum.Value - self.Minimum.Value

    def Contains(self, value: AxisValue):
        return self.Minimum.Value <= value.Value <= self.Maximum.Value

    def Union(self, other: Optional['AxisRange']):
        if other is None:
            return self
        return AxisRange(
            AxisValue(min(self.Minimum.Value, other.Minimum.Value)),
            AxisValue(max(self.Maximum.Value, other.Maximum.Value))
        )

    def Intersect(self, other: 'AxisRange'):
        return AxisRange(
            AxisValue(max(self.Minimum.Value, other.Minimum.Value)),
            AxisValue(min(self.Maximum.Value, other.Maximum.Value))
        )


class IChartMargin(ABC):
    @abstractmethod
    def Add(self, low: float, high: float):
        pass


class RelativeMargin(IChartMargin):
    def __init__(self, left: float, right: float):
        self.left = left
        self.right = right

    def Add(self, low: float, high: float):
        return low + self.left, high - self.right


class BaseAxisManager(Generic[T], ABC):
    EPS = 1e-10

    def __init__(self, range: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[IChartMargin] = None):
        self.InitialRangeCore = range
        self.InitialRange = self.CoerceRange(self.InitialRangeCore, bounds)
        self.Bounds = bounds
        self.ChartMargin = margin or RelativeMargin(0, 0)
        self.Range = self.InitialRange

        self.labelTicks = None
        self.unitLabel = ""

    @staticmethod
    def CoerceRange(r: AxisRange, bound: Optional[AxisRange]):
        range_ = r.Union(bound)
        if range_.Delta <= BaseAxisManager.EPS:
            range_ = AxisRange(
                AxisValue(range_.Minimum.Value - 1),
                AxisValue(range_.Maximum.Value + 1)
            )
        return range_

    @property
    def Min(self):
        return self.Range.Minimum

    @property
    def Max(self):
        return self.Range.Maximum

    @property
    def LabelTicks(self):
        return self.labelTicks or self.GetLabelTicks()

    @LabelTicks.setter
    def LabelTicks(self, value):
        self.labelTicks = value

    @property
    def UnitLabel(self):
        return self.unitLabel

    @UnitLabel.setter
    def UnitLabel(self, value):
        self.unitLabel = value

    def UpdateInitialRange(self, range: AxisRange):
        self.InitialRangeCore = range
        self.InitialRange = self.CoerceRange(range, self.Bounds)
        self.Range = self.InitialRange
        self.OnInitialRangeChanged()

    def Contains(self, value: AxisValue):
        return self.InitialRange.Contains(value)

    def ContainsCurrent(self, value: AxisValue):
        return self.Range.Contains(value)

    def Focus(self, range: AxisRange):
        self.Range = range.Union(self.Bounds).Intersect(self.InitialRange)

    def Recalculate(self, drawableLength: float):
        if drawableLength == 0:
            return
        lo, hi = self.ChartMargin.Add(0, drawableLength)
        self.InitialRange = self.TranslateFromRelativeRange(
            lo / drawableLength,
            hi / drawableLength,
            self.CoerceRange(self.InitialRangeCore, self.Bounds)
        )

    def Reset(self):
        self.Focus(self.InitialRange)

    @abstractmethod
    def GetLabelTicks(self) -> List:
        pass

    @abstractmethod
    def TranslateToAxisValue(self, value: T) -> AxisValue:
        pass

    def TranslateToAxisValueGeneric(self, value: Union[T, object]) -> AxisValue:
        try:
            return self.TranslateToAxisValue(value)
        except Exception:
            return AxisValue(math.nan)

    def TranslateRelativePointCore(self, value: AxisValue, min_: AxisValue, max_: AxisValue):
        return (value.Value - min_.Value) / (max_.Value - min_.Value)

    def TranslateToRelativePoints(self, values: List[T]):
        max_ = self.Max
        min_ = self.Min
        return [self.TranslateRelativePointCore(self.TranslateToAxisValue(value), min_, max_) for value in values]

    def FlipRelative(self, relative: float, isFlipped: bool):
        return 1 - relative if isFlipped else relative

    def TranslateToRenderPoint(self, value: AxisValue, isFlipped: bool, drawableLength: float):
        return self.FlipRelative(self.TranslateRelativePointCore(value, self.Min, self.Max), isFlipped) * drawableLength

    def TranslateFromRelativePoint(self, value: float, range: AxisRange):
        return AxisValue(value * (range.Maximum.Value - range.Minimum.Value) + range.Minimum.Value)

    def TranslateFromRelativeRange(self, low: float, hi: float, range: AxisRange):
        return AxisRange(
            self.TranslateFromRelativePoint(low, range),
            self.TranslateFromRelativePoint(hi, range)
        )

    def TranslateFromRenderPoint(self, value: float, isFlipped: bool, drawableLength: float):
        return self.TranslateFromRelativePoint(self.FlipRelative(value / drawableLength, isFlipped))

    def TranslateToRenderPoints(self, values: List[T], isFlipped: bool, drawableLength: float):
        results = self.TranslateToRelativePoints(values)
        return [self.FlipRelative(result, isFlipped) * drawableLength for result in results]
