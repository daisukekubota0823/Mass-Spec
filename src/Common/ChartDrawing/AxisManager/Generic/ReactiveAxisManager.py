from typing import Generic, TypeVar, List, Callable, Optional, Tuple
from rx import Observable
from rx.core.typing import Observer
from rx.subject import Subject

T = TypeVar("T")


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


class BaseAxisManager(Generic[T]):
    def __init__(self, range_: AxisRange):
        self.Range = range_
        self.UnitLabel = ""
        self.RangeChanged = Subject()  # Observable for range changes
        self.InitialRangeChanged = Subject()
        self.AxisValueMappingChanged = Subject()

    def Contains(self, value: AxisValue) -> bool:
        return True

    def ContainsCurrent(self, value: AxisValue) -> bool:
        return True

    def Focus(self, range_: AxisRange):
        pass

    def GetLabelTicks(self) -> List[LabelTickData]:
        return []

    def Recalculate(self, drawable_length: float):
        pass

    def Reset(self):
        pass

    def TranslateFromRenderPoint(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
        return AxisValue(0)

    def TranslateToAxisValue(self, value: T) -> AxisValue:
        return AxisValue(0)

    def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
        return 0.0

    def TranslateToRenderPoints(self, values: List[T], is_flipped: bool, drawable_length: float) -> List[float]:
        return [0.0 for _ in values]


class ReactiveAxisManager(Generic[T]):
    def __init__(self, axis_manager: BaseAxisManager[T], range_source: Observable):
        self.AxisManagerImpl = axis_manager

        self.range_observer = RangeObserver(self.AxisManagerImpl)
        self.range_observer.subscribe(range_source)

    @property
    def Range(self) -> AxisRange:
        return self.AxisManagerImpl.Range

    @property
    def UnitLabel(self) -> str:
        return self.AxisManagerImpl.UnitLabel

    def Contains(self, value: AxisValue) -> bool:
        return self.AxisManagerImpl.Contains(value)

    def ContainsCurrent(self, value: AxisValue) -> bool:
        return self.AxisManagerImpl.ContainsCurrent(value)

    def Focus(self, range_: AxisRange):
        self.AxisManagerImpl.Focus(range_)

    def GetLabelTicks(self) -> List[LabelTickData]:
        return self.AxisManagerImpl.GetLabelTicks()

    def Recalculate(self, drawable_length: float):
        self.AxisManagerImpl.Recalculate(drawable_length)

    def Reset(self):
        self.AxisManagerImpl.Reset()

    def TranslateFromRenderPoint(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
        return self.AxisManagerImpl.TranslateFromRenderPoint(value, is_flipped, drawable_length)

    def TranslateToAxisValue(self, value: T) -> AxisValue:
        return self.AxisManagerImpl.TranslateToAxisValue(value)

    def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
        return self.AxisManagerImpl.TranslateToRenderPoint(value, is_flipped, drawable_length)

    def TranslateToRenderPoints(self, values: List[T], is_flipped: bool, drawable_length: float) -> List[float]:
        return self.AxisManagerImpl.TranslateToRenderPoints(values, is_flipped, drawable_length)


class RangeObserver(Observer):
    def __init__(self, axis: BaseAxisManager[T]):
        self.axis = axis

    def on_next(self, value):
        if isinstance(value, AxisRange):
            self.axis.UpdateInitialRange(value)
        elif isinstance(value, tuple) and len(value) == 2:
            low, high = value
            self.axis.UpdateInitialRange(AxisRange(low, high))

    def on_error(self, error: Exception):
        print(f"Error: {error}")

    def on_completed(self):
        print("Observation completed")


# Static methods equivalent
class ReactiveAxisManagerFactory:
    @staticmethod
    def to_reactive_log_scale_axis_manager(range_source: Observable, low_bound: Optional[T] = None, high_bound: Optional[T] = None):
        if low_bound is not None and high_bound is not None:
            axis_manager = BaseAxisManager(AxisRange(low_bound, high_bound))
        else:
            axis_manager = BaseAxisManager(AxisRange(0, 1))
        return ReactiveAxisManager(axis_manager, range_source)

    @staticmethod
    def to_reactive_continuous_axis_manager(range_source: Observable, low_bound: T, high_bound: T):
        axis_manager = BaseAxisManager(AxisRange(low_bound, high_bound))
        return ReactiveAxisManager(axis_manager, range_source)
