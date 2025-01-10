from typing import List, Optional
import math


class AxisValue:
    def __init__(self, value: float):
        self.value = value


class AxisRange:
    def __init__(self, minimum: AxisValue, maximum: AxisValue):
        self.Minimum = minimum
        self.Maximum = maximum


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


class IChartMargin:
    pass


class BaseAxisManager:
    def __init__(self, range_: AxisRange, margin: Optional[IChartMargin] = None, bounds: Optional[AxisRange] = None):
        self.Range = range_
        self.Margin = margin
        self.Bounds = bounds
        self.InitialRangeCore = range_
        self.labelTicks = None
        self.UnitLabel = ""

    def CoerceRange(self, range_: AxisRange, bounds: Optional[AxisRange]) -> AxisRange:
        if bounds is None:
            return range_
        return AxisRange(
            AxisValue(max(range_.Minimum.value, bounds.Minimum.value)),
            AxisValue(min(range_.Maximum.value, bounds.Maximum.value))
        )

    def GetLabelTicks(self) -> List[LabelTickData]:
        raise NotImplementedError

    def TranslateToAxisValue(self, value: float) -> AxisValue:
        raise NotImplementedError


class SqrtAxisManager(BaseAxisManager):
    def __init__(self, range_: AxisRange, margin: Optional[IChartMargin] = None, bounds: Optional[AxisRange] = None):
        super().__init__(range_, margin, bounds)
        self._labelType = LabelType.Standard
        self._labelGenerator = None

    @property
    def LabelType(self):
        return self._labelType

    @LabelType.setter
    def LabelType(self, value):
        self._labelType = value
        self._labelGenerator = None  # Reset label generator when label type changes

    @property
    def LabelGenerator(self):
        if self._labelType == LabelType.Order:
            if not isinstance(self._labelGenerator, OrderLabelGenerator):
                self._labelGenerator = OrderLabelGenerator()
        elif self._labelType == LabelType.Relative:
            if not isinstance(self._labelGenerator, RelativeLabelGenerator):
                self._labelGenerator = RelativeLabelGenerator()
        elif self._labelType == LabelType.Percent:
            if not isinstance(self._labelGenerator, PercentLabelGenerator):
                self._labelGenerator = PercentLabelGenerator()
        else:  # Standard
            if not isinstance(self._labelGenerator, StandardLabelGenerator):
                self._labelGenerator = StandardLabelGenerator()
        return self._labelGenerator

    def OnRangeChanged(self):
        self.labelTicks = None
        # Call base class method if needed

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

    def TranslateToAxisValue(self, value: float) -> AxisValue:
        return AxisValue(math.sqrt(value))

    @staticmethod
    def ConvertToAxisValue(value: float) -> AxisValue:
        return AxisValue(math.sqrt(value))

    @staticmethod
    def ConvertToRange(low: float, high: float) -> AxisRange:
        return AxisRange(SqrtAxisManager.ConvertToAxisValue(low), SqrtAxisManager.ConvertToAxisValue(high))
