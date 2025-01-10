from typing import List, Callable, TypeVar, Generic, Optional, Iterable
import math

T = TypeVar('T')
U = TypeVar('U')


class AxisValue:
    def __init__(self, value: float):
        self.value = value


class AxisRange:
    def __init__(self, minimum: float, maximum: float):
        self.Minimum = AxisValue(minimum)
        self.Maximum = AxisValue(maximum)


class LabelTickData:
    def __init__(self):
        pass


class LabelType:
    Standard = "Standard"
    Order = "Order"
    Relative = "Relative"
    Percent = "Percent"


class ILabelGenerator:
    def Generate(self, min_val: float, max_val: float, initial_min: float, initial_max: float):
        return [], ""


class RelativeLabelGenerator(ILabelGenerator):
    pass


class PercentLabelGenerator(ILabelGenerator):
    pass


class LogScaleLabelGenerator(ILabelGenerator):
    pass


class BaseSelectableLogScaleLabelGenerator(ILabelGenerator):
    def __init__(self, base_: int):
        self.base = base_


class IChartMargin:
    pass


class BaseAxisManager(Generic[T]):
    def __init__(self, range_: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[IChartMargin] = None):
        self.InitialRangeCore = range_
        self.Bounds = bounds
        self.Range = self.CoerceRange(range_, bounds)
        self.ChartMargin = margin
        self.labelTicks = None
        self.UnitLabel = ""

    @staticmethod
    def CoerceRange(range_: AxisRange, bounds: Optional[AxisRange]) -> AxisRange:
        if bounds is None:
            return range_
        return AxisRange(
            max(range_.Minimum.value, bounds.Minimum.value),
            min(range_.Maximum.value, bounds.Maximum.value),
        )

    def UpdateInitialRange(self, range_: AxisRange):
        self.InitialRangeCore = range_
        self.Range = self.CoerceRange(range_, self.Bounds)

    def GetLabelTicks(self) -> List[LabelTickData]:
        raise NotImplementedError

    def TranslateToAxisValue(self, value: T) -> AxisValue:
        raise NotImplementedError


class LogScaleAxisManager(BaseAxisManager[T]):
    def __init__(self, range_: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[IChartMargin] = None, base_: int = 10):
        super().__init__(range_, bounds, margin)
        self.Base = base_
        self._labelType = LabelType.Standard
        self._labelGenerator = BaseSelectableLogScaleLabelGenerator(base_) if base_ != 10 else LogScaleLabelGenerator()

    @property
    def LabelType(self):
        return self._labelType

    @LabelType.setter
    def LabelType(self, value):
        self._labelType = value
        self._labelGenerator = None  # Reset label generator when label type changes

    @property
    def LabelGenerator(self):
        if self._labelType == LabelType.Relative:
            if not isinstance(self._labelGenerator, RelativeLabelGenerator):
                self._labelGenerator = RelativeLabelGenerator()
        elif self._labelType == LabelType.Percent:
            if not isinstance(self._labelGenerator, PercentLabelGenerator):
                self._labelGenerator = PercentLabelGenerator()
        else:  # Standard or Order
            if not isinstance(self._labelGenerator, (LogScaleLabelGenerator, BaseSelectableLogScaleLabelGenerator)):
                self._labelGenerator = LogScaleLabelGenerator()
        return self._labelGenerator

    def UpdateInitialRange(self, low: T, high: T):
        self.UpdateInitialRange(AxisRange(self.ConvertToAxisValue(low).value, self.ConvertToAxisValue(high).value))

    def GetLabelTicks(self) -> List[LabelTickData]:
        initial_range_core = self.CoerceRange(self.InitialRangeCore, self.Bounds)
        ticks, self.UnitLabel = self.LabelGenerator.Generate(
            self.Range.Minimum.value,
            self.Range.Maximum.value,
            initial_range_core.Minimum.value,
            initial_range_core.Maximum.value,
        )
        return ticks

    def TranslateToAxisValue(self, value: T) -> AxisValue:
        return self.ConvertToAxisValue(value)

    @staticmethod
    def ConvertToAxisValue(value: T, base_: int = 10) -> AxisValue:
        return AxisValue(math.log(float(value), base_))

    @staticmethod
    def Build(source: Iterable[U], map_func: Callable[[U], T]) -> "LogScaleAxisManager[T]":
        mapped_values = list(map(map_func, source))
        return LogScaleAxisManager(AxisRange(min(mapped_values), max(mapped_values)))

    @staticmethod
    def BuildWithBounds(source: Iterable[U], map_func: Callable[[U], T], low_bound: T, high_bound: T) -> "LogScaleAxisManager[T]":
        mapped_values = list(map(map_func, source))
        return LogScaleAxisManager(
            AxisRange(min(mapped_values), max(mapped_values)),
            bounds=AxisRange(
                LogScaleAxisManager.ConvertToAxisValue(low_bound).value,
                LogScaleAxisManager.ConvertToAxisValue(high_bound).value,
            ),
        )
