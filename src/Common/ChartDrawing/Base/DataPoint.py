from dataclasses import dataclass, field
    from typing import Callable, Optional


    class Observable:
        """Base class to implement property change notification."""
        def __init__(self):
            self._property_changed_listeners = []

        def add_property_changed_listener(self, listener: Callable[[str], None]):
            self._property_changed_listeners.append(listener)

        def remove_property_changed_listener(self, listener: Callable[[str], None]):
            self._property_changed_listeners.remove(listener)

        def raise_property_changed(self, property_name: str):
            for listener in self._property_changed_listeners:
                listener(property_name)


    class DataPoint(Observable):
        _member_id = 0

        def __init__(self, x: float = 0.0, y: float = 0.0, point_type: int = 0):
            super().__init__()
            self._x = x
            self._y = y
            self._type = point_type
            self._id = DataPoint._member_id
            DataPoint._member_id += 1

        @property
        def x(self) -> float:
            return self._x

        @x.setter
        def x(self, value: float):
            if self._x != value:
                self._x = value
                self.raise_property_changed("x")

        @property
        def y(self) -> float:
            return self._y

        @y.setter
        def y(self, value: float):
            if self._y != value:
                self._y = value
                self.raise_property_changed("y")

        @property
        def type(self) -> int:
            return self._type

        @type.setter
        def type(self, value: int):
            if self._type != value:
                self._type = value
                self.raise_property_changed("type")

        @property
        def id(self) -> int:
            return self._id

        def clone(self) -> "DataPoint":
            return DataPoint(self._x, self._y, self._type)

        def __str__(self) -> str:
            return f"X={self._x} Y={self._y} Type={self._type} ID={self._id}"
    