from typing import Callable, Dict, List, TypeVar, Generic, Iterable, Optional, Set
    from collections import defaultdict

    T = TypeVar('T')
    U = TypeVar('U')


    class AxisValue:
        def __init__(self, value: float):
            self.value = value

        @staticmethod
        def NaN():
            return AxisValue(float('nan'))


    class AxisRange:
        def __init__(self, minimum: float, maximum: float):
            self.Minimum = AxisValue(minimum)
            self.Maximum = AxisValue(maximum)


    class LabelTickData:
        def __init__(self, label: str, tick_type: str, center: AxisValue, width: float, source: T):
            self.Label = label
            self.TickType = tick_type
            self.Center = center
            self.Width = width
            self.Source = source


    class TickType:
        LongTick = "LongTick"


    class RelativeMargin:
        def __init__(self, margin: float):
            self.margin = margin


    class BaseAxisManager(Generic[T]):
        def __init__(self, range_: AxisRange):
            self.InitialRange = range_
            self.ChartMargin = None

        def UpdateInitialRange(self, range_: AxisRange):
            self.InitialRange = range_

        def GetLabelTicks(self) -> List[LabelTickData]:
            raise NotImplementedError

        def TranslateToAxisValue(self, value: T) -> AxisValue:
            raise NotImplementedError


    class CategoryAxisManager(Generic[U, T], BaseAxisManager[T]):
        def __init__(
            self,
            collection: Iterable[T],
            to_key: Callable[[T], U],
            to_label: Optional[Callable[[T], str]] = None,
        ):
            super().__init__(self._count_element(collection, to_key))
            self.collection = list(collection)
            self.to_key = to_key
            self.to_label = to_label or self._to_string
            self.converter = self._to_dictionary(self.collection, to_key)
            self.ChartMargin = RelativeMargin(0.05)

        @staticmethod
        def _count_element(collection: Iterable[T], to_key: Callable[[T], U]) -> AxisRange:
            unique_keys: Set[U] = set(map(to_key, collection))
            return AxisRange(0.0, len(unique_keys))

        @staticmethod
        def _to_dictionary(collection: Iterable[T], to_key: Callable[[T], U]) -> Dict[U, AxisValue]:
            result = {}
            idx = 0
            for item in collection:
                key = to_key(item)
                if key not in result:
                    result[key] = AxisValue(0.5 + idx)
                    idx += 1
            return result

        def UpdateCollection(self, collection: Iterable[T]):
            self.collection = list(collection)
            self.converter = self._to_dictionary(self.collection, self.to_key)
            self.UpdateInitialRange(self._count_element(self.collection, self.to_key))

        @staticmethod
        def _to_string(value: T) -> str:
            return str(value)

        def GetLabelTicks(self) -> List[LabelTickData]:
            result = []
            for item in self.collection:
                result.append(LabelTickData(
                    label=self.to_label(item),
                    tick_type=TickType.LongTick,
                    center=self.converter[self.to_key(item)],
                    width=1.0,
                    source=item,
                ))
            return result

        def TranslateToAxisValue(self, value: T) -> AxisValue:
            key = self.to_key(value)
            if key in self.converter:
                return self.converter[key]
            return AxisValue.NaN()


    class CategoryAxisManagerSingle(Generic[T], CategoryAxisManager[T, T]):
        def __init__(self, collection: Iterable[T], to_label: Optional[Callable[[T], str]] = None):
            super().__init__(collection, self._identity, to_label)

        @staticmethod
        def _identity(value: T) -> T:
            return value
    