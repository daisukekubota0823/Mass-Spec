from typing import List, Optional
import math


class AxisValue:
    def __init__(self, value: float):
        self.value = value

    def __add__(self, other):
        if isinstance(other, AxisValue):
            return AxisValue(self.value + other.value)
        return AxisValue(self.value + other)

    def __mul__(self, factor):
        return AxisValue(self.value * factor)


class AxisRange:
    def __init__(self, minimum: float, maximum: float):
        self.Minimum = AxisValue(minimum)
        self.Maximum = AxisValue(maximum)

    def __add__(self, other):
        if isinstance(other, AxisValue):
            return AxisRange(self.Minimum.value + other.value, self.Maximum.value + other.value)
        return AxisRange(self.Minimum.value + other, self.Maximum.value + other)

    def __mul__(self, factor):
        return AxisRange(self.Minimum.value * factor, self.Maximum.value * factor)


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

    def TranslateToAxisValue(self, value: float) -> AxisValue:
        raise NotImplementedError


class DefectAxisManager(BaseAxisManager):
    DEFECT_RANGE = AxisRange(-0.5, 0.5)

    def __init__(self, divisor: float, factor: Optional[float] = None, margin: Optional[IChartMargin] = None, bounds: Optional[AxisRange] = None):
        if factor is not None:
            super().__init__((self.DEFECT_RANGE + AxisValue(0.5)) * factor, margin, bounds)
            self.Factor = factor
        else:
            super().__init__(self.DEFECT_RANGE, margin, bounds)
        self.Divisor = divisor
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

    @property
    def Divisor(self):
        return self._divisor

    @Divisor.setter
    def Divisor(self, value):
        self._divisor = value
        self.OnAxisValueMappingChanged()

    @property
    def Factor(self):
        return self._factor

    @Factor.setter
    def Factor(self, value):
        self._factor = value
        self.OnAxisValueMappingChanged()
        self.UpdateInitialRange((self.DEFECT_RANGE + 0.5) * self.Factor)

    def OnAxisValueMappingChanged(self):
        # Placeholder for event handling
        pass

    def OnRangeChanged(self):
        self.labelTicks = None
        # Call base class method if needed
        pass

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
        if self.Factor != 0:
            return AxisValue((value / self.Divisor - math.floor(value / self.Divisor)) * self.Factor)
        else:
            return AxisValue(value / self.Divisor - round(value / self.Divisor))
