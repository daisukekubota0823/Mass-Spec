from typing import List, Generic, TypeVar, Iterable

    T = TypeVar('T')


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


    class IAxisManager(Generic[T]):
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

        def TranslateToAxisValue(self, value: T) -> AxisValue:
            raise NotImplementedError

        def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
            raise NotImplementedError

        def TranslateToRenderPoints(self, values: Iterable[T], is_flipped: bool, drawable_length: float) -> List[float]:
            raise NotImplementedError


    class ConstantAxisManager(IAxisManager[T]):
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super(ConstantAxisManager, cls).__new__(cls)
            return cls._instance

        def __init__(self):
            self.Range = AxisRange(AxisValue(-1.0), AxisValue(1.0))

        @staticmethod
        def Instance():
            return ConstantAxisManager()

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
            return AxisValue(0.0)

        def TranslateToAxisValue(self, value: T) -> AxisValue:
            return AxisValue(0.0)

        def TranslateToRenderPoint(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
            return 0.5 * drawable_length

        def TranslateToRenderPoints(self, values: Iterable[T], is_flipped: bool, drawable_length: float) -> List[float]:
            return [0.5 * drawable_length for _ in values]


    class ConstantAxisManagerStatic:
        _instance = None

        @staticmethod
        def Instance():
            if ConstantAxisManagerStatic._instance is None:
                ConstantAxisManagerStatic._instance = ConstantAxisManager()
            return ConstantAxisManagerStatic._instance
    