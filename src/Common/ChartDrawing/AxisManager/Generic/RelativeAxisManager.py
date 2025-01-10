from typing import List, Optional, Iterable, Union


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


class IChartMargin:
    pass


class IAxisManager:
    def __init__(self):
        pass

    def Contains(self, value: AxisValue) -> bool:
        raise NotImplementedError

    def ContainsCurrent(self, value: AxisValue) -> bool:
        raise NotImplementedError

    def Focus(self, range_: AxisRange):
        raise NotImplementedError

    def GetLabelTicks(self) -> List[LabelTickData]:
        raise NotImplementedError

    def Recalculate(self, drawable_length: float):
        raise NotImplementedError

    def Reset(self):
        raise NotImplementedError

    def TranslateFromRenderPoint(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
        raise NotImplementedError

    def TranslateToAxisValue(self, value: Union[float, object]) -> AxisValue:
        raise NotImplementedError

    def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
        raise NotImplementedError

    def TranslateToRenderPoints(self, values: Iterable[Union[float, AxisValue]], is_flipped: bool, drawable_length: float) -> List[float]:
        raise NotImplementedError


class ContinuousAxisManager(IAxisManager):
    def __init__(self, range_: AxisRange, margin: Optional[IChartMargin] = None, bounds: Optional[AxisRange] = None):
        super().__init__()
        self.Range = range_
        self.Margin = margin
        self.Bounds = bounds

    def Contains(self, value: AxisValue) -> bool:
        return True

    def GetLabelTicks(self) -> List[LabelTickData]:
        return []


class RelativeAxisManager(IAxisManager):
    RELATIVE_RANGE = AxisRange(0.0, 1.0)

    def __init__(self, low: float, high: float, share_axis: Optional[IAxisManager] = None):
        self.Low = low
        self.High = high
        self.Delta = high - low
        self._axis_manager_impl = share_axis or ContinuousAxisManager(self.RELATIVE_RANGE)

    @property
    def Range(self) -> AxisRange:
        return AxisRange(
            self._axis_manager_impl.Range.Minimum.value * self.Delta + self.Low,
            self._axis_manager_impl.Range.Maximum.value * self.Delta + self.Low
        )

    def Contains(self, value: AxisValue) -> bool:
        return self._axis_manager_impl.Contains(value)

    def ContainsCurrent(self, value: AxisValue) -> bool:
        return self._axis_manager_impl.ContainsCurrent(value)

    def Focus(self, range_: AxisRange):
        self._axis_manager_impl.Focus(range_)

    def GetLabelTicks(self) -> List[LabelTickData]:
        return self._axis_manager_impl.GetLabelTicks()

    def Recalculate(self, drawable_length: float):
        self._axis_manager_impl.Recalculate(drawable_length)

    def Reset(self):
        self._axis_manager_impl.Reset()

    def TranslateFromRenderPoint(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
        return self._axis_manager_impl.TranslateFromRenderPoint(value, is_flipped, drawable_length)

    def TranslateToAxisValue(self, value: Union[float, object]) -> AxisValue:
        if isinstance(value, float):
            return self._axis_manager_impl.TranslateToAxisValue((value - self.Low) / self.Delta)
        elif isinstance(value, object):
            return self.TranslateToAxisValue(float(value))

    def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
        return self._axis_manager_impl.TranslateToRenderPoint(value, is_flipped, drawable_length)

    def TranslateToRenderPoints(self, values: Iterable[Union[float, object]], is_flipped: bool, drawable_length: float) -> List[float]:
        normalized_values = [(val - self.Low) / self.Delta if isinstance(val, float) else val for val in values]
        return self._axis_manager_impl.TranslateToRenderPoints(normalized_values, is_flipped, drawable_length)

    @staticmethod
    def CreateBaseAxis(bounds: Optional[AxisRange] = None, margin: Optional[IChartMargin] = None) -> IAxisManager:
        if bounds and margin:
            return ContinuousAxisManager(RelativeAxisManager.RELATIVE_RANGE, margin, bounds)
        elif bounds:
            return ContinuousAxisManager(RelativeAxisManager.RELATIVE_RANGE, bounds=bounds)
        elif margin:
            return ContinuousAxisManager(RelativeAxisManager.RELATIVE_RANGE, margin=margin)
        else:
            return ContinuousAxisManager(RelativeAxisManager.RELATIVE_RANGE)
