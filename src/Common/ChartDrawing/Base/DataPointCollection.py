from typing import List, Iterable
    from collections.abc import MutableSequence


    class DataPoint:
        def __init__(self, x: float = 0.0, y: float = 0.0, point_type: int = 0):
            self.x = x
            self.y = y
            self.type = point_type

        def clone(self) -> "DataPoint":
            return DataPoint(self.x, self.y, self.type)

        def __repr__(self):
            return f"DataPoint(x={self.x}, y={self.y}, type={self.type})"


    class DataPointCollection(MutableSequence):
        def __init__(self, points: Iterable[DataPoint] = None):
            self._items: List[DataPoint] = list(points) if points else []

        def __getitem__(self, index: int) -> DataPoint:
            return self._items[index]

        def __setitem__(self, index: int, value: DataPoint):
            self._items[index] = value

        def __delitem__(self, index: int):
            del self._items[index]

        def __len__(self) -> int:
            return len(self._items)

        def insert(self, index: int, value: DataPoint):
            self._items.insert(index, value)

        def accumulate(self) -> "DataPointCollection":
            result = [item.clone() for item in self._items]

            type_to_acc = {item.type: 0.0 for item in result}
            for item in result:
                type_to_acc[item.type] += item.y
                item.y = type_to_acc[item.type]

            return DataPointCollection(result)

        def __repr__(self):
            return f"DataPointCollection({self._items})"
    