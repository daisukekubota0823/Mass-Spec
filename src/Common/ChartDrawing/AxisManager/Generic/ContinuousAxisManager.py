from typing import List, TypeVar, Generic, Callable, Iterable, Optional
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


class OrderLabelGenerator(ILabelGenerator):
    pass


class RelativeLabelGenerator(ILabelGenerator):
    pass


class PercentLabelGenerator(ILabelGenerator):
    pass


class StandardLabelGenerator(ILabelGenerator):
    pass


class BaseAxisManager(Generic[T]):
    def __init__(self, range_: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[float] = None):
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


class ContinuousAxisManager(BaseAxisManager[T]):
    def __init__(self, range_: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[float] = None):
        super().__init__(range_, bounds, margin)
        self.labelType = LabelType.Standard
        self.labelGenerator = None

    @property
    def LabelType(self):
        return self.labelType

    @LabelType.setter
    def LabelType(self, value):
        self.labelType = value
        self.labelGenerator = None  # Reset the generator when label type changes

    @property
    def LabelGenerator(self):
        if self.labelType == LabelType.Order:
            if not isinstance(self.labelGenerator, OrderLabelGenerator):
                self.labelGenerator = OrderLabelGenerator()
        elif self.labelType == LabelType.Relative:
            if not isinstance(self.labelGenerator, RelativeLabelGenerator):
                self.labelGenerator = RelativeLabelGenerator()
        elif self.labelType == LabelType.Percent:
            if not isinstance(self.labelGenerator, PercentLabelGenerator):
                self.labelGenerator = PercentLabelGenerator()
        else:  # Standard
            if not isinstance(self.labelGenerator, StandardLabelGenerator):
                self.labelGenerator = StandardLabelGenerator()
        return self.labelGenerator

    def UpdateInitialRange(self, low: T, high: T):
        self.UpdateInitialRange(AxisRange(float(low), float(high)))

    def GetLabelTicks(self) -> List[LabelTickData]:
        generator = self.LabelGenerator
        initial_range_core = self.CoerceRange(self.InitialRangeCore, self.Bounds)
        ticks, self.UnitLabel = generator.Generate(
            self.Range.Minimum.value,
            self.Range.Maximum.value,
            initial_range_core.Minimum.value,
            initial_range_core.Maximum.value,
        )
        return ticks

    def TranslateToAxisValue(self, value: T) -> AxisValue:
        return AxisValue(float(value))

    @staticmethod
    def Build(source: Iterable[U], map_func: Callable[[U], T]) -> "ContinuousAxisManager[T]":
        mapped_values = list(map(map_func, source))
        return ContinuousAxisManager(AxisRange(min(mapped_values), max(mapped_values)))

    @staticmethod
    def BuildWithBounds(source: Iterable[U], map_func: Callable[[U], T], bounds: AxisRange) -> "ContinuousAxisManager[T]":
        mapped_values = list(map(map_func, source))
        return ContinuousAxisManager(AxisRange(min(mapped_values), max(mapped_values)), bounds)
