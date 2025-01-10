from typing import List, Optional, Iterable, Union
import math


class AxisValue:
    def __init__(self, value: float):
        self.Value = value

    def __repr__(self):
        return f"AxisValue({self.Value})"


class AxisRange:
    def __init__(self, minimum: float, maximum: float):
        self.Minimum = AxisValue(minimum)
        self.Maximum = AxisValue(maximum)

    def Intersect(self, other: 'AxisRange') -> 'AxisRange':
        return AxisRange(
            max(self.Minimum.Value, other.Minimum.Value),
            min(self.Maximum.Value, other.Maximum.Value)
        )

    def Union(self, other: 'AxisRange') -> 'AxisRange':
        return AxisRange(
            min(self.Minimum.Value, other.Minimum.Value),
            max(self.Maximum.Value, other.Maximum.Value)
        )

    def Contains(self, value: AxisValue) -> bool:
        return self.Minimum.Value <= value.Value <= self.Maximum.Value

    def __repr__(self):
        return f"AxisRange(Minimum={self.Minimum}, Maximum={self.Maximum})"


class LabelTickData:
    def __init__(self, label: str, tick_type: str, center: float, width: float, source: float):
        self.Label = label
        self.TickType = tick_type
        self.Center = center
        self.Width = width
        self.Source = source


class FreezableAxisManager:
    def __init__(self):
        self.Range = AxisRange(0, 1)
        self.Bounds = None  # Type: Optional[AxisRange]
        self.InitialRange = AxisRange(0, 1)
        self.LabelTicks: List[LabelTickData] = []
        self.ShouldCoerceLabelTicksChanged = False
        self.RangeChanged = None  # Event handler placeholder
        self.InitialRangeChanged = None  # Event handler placeholder
        self.AxisValueMappingChanged = None  # Event handler placeholder

    @property
    def Min(self) -> AxisValue:
        return self.Range.Minimum

    @Min.setter
    def Min(self, value: AxisValue):
        self.Focus(AxisRange(value.Value, self.Range.Maximum.Value))

    @property
    def Max(self) -> AxisValue:
        return self.Range.Maximum

    @Max.setter
    def Max(self, value: AxisValue):
        self.Focus(AxisRange(self.Range.Minimum.Value, value.Value))

    def Focus(self, range_: AxisRange):
        self.Range = range_
        # Trigger RangeChanged event if needed
        if self.RangeChanged:
            self.RangeChanged(self, None)

    def Reset(self):
        self.Focus(self.InitialRange)

    def Recalculate(self, drawable_length: float):
        # Placeholder for recalculation logic
        pass

    def Contains(self, val: AxisValue) -> bool:
        return self.InitialRange.Minimum.Value <= val.Value <= self.InitialRange.Maximum.Value

    def ContainsCurrent(self, value: AxisValue) -> bool:
        return self.Range.Contains(value)

    def GetLabelTicks(self) -> List[LabelTickData]:
        # Abstract method placeholder
        raise NotImplementedError

    def FlipRelative(self, relative: float, is_flipped: bool) -> float:
        return 1 - relative if is_flipped else relative

    def TranslateToRelativePointCore(self, value: AxisValue, min_: AxisValue, max_: AxisValue) -> float:
        return (value.Value - min_.Value) / (max_.Value - min_.Value)

    def TranslateToAxisValue(self, value: Union[str, float, int]) -> AxisValue:
        try:
            if isinstance(value, str):
                return AxisValue(float(value))
            elif isinstance(value, (float, int)):
                return AxisValue(float(value))
        except ValueError:
            pass
        return AxisValue(float('nan'))

    def TranslateToRelativePoints(self, values: Iterable[Union[AxisValue, float]]) -> List[float]:
        min_ = self.Min.Value
        max_ = self.Max.Value
        return [
            self.TranslateToRelativePointCore(self.TranslateToAxisValue(value), self.Min, self.Max)
            for value in values
        ]

    def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
        relative = self.TranslateToRelativePointCore(value, self.Min, self.Max)
        return self.FlipRelative(relative, is_flipped) * drawable_length

    def TranslateToRenderPoints(self, values: Iterable[Union[AxisValue, float]], is_flipped: bool, drawable_length: float) -> List[float]:
        relative_points = self.TranslateToRelativePoints(values)
        return [self.FlipRelative(point, is_flipped) * drawable_length for point in relative_points]

    def TranslateFromRelativePointCore(self, value: float, min_: float, max_: float) -> AxisValue:
        return AxisValue(value * (max_ - min_) + min_)

    def TranslateFromRenderPoint(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
        relative = self.FlipRelative(value / drawable_length, is_flipped)
        return self.TranslateFromRelativePointCore(relative, self.Min.Value, self.Max.Value)
