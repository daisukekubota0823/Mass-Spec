from typing import Tuple


    class BindableBase:
        """Base class to simulate property change notification."""
        def __init__(self):
            self._property_changed_listeners = []

        def add_property_changed_listener(self, listener):
            self._property_changed_listeners.append(listener)

        def remove_property_changed_listener(self, listener):
            self._property_changed_listeners.remove(listener)

        def notify_property_changed(self, property_name: str):
            for listener in self._property_changed_listeners:
                listener(property_name)

        def set_property(self, attr_name: str, value):
            if getattr(self, attr_name) != value:
                setattr(self, attr_name, value)
                self.notify_property_changed(attr_name)


    class AxisRange:
        """Placeholder for AxisRange."""
        def __init__(self, minimum: float, maximum: float):
            self.minimum = minimum
            self.maximum = maximum


    class IAxisManager:
        """Placeholder for IAxisManager interface."""
        def translate_to_axis_value(self, value: float) -> float:
            raise NotImplementedError("This method should be implemented in subclasses.")


    class RangeSelection(BindableBase):
        def __init__(self, range_: AxisRange):
            super().__init__()
            self._range = range_
            self._is_selected = False
            self._color = "gray"  # Default color as a string representation.

        @property
        def range(self) -> AxisRange:
            return self._range

        @property
        def is_selected(self) -> bool:
            return self._is_selected

        @is_selected.setter
        def is_selected(self, value: bool):
            self.set_property('_is_selected', value)

        @property
        def color(self) -> str:
            return self._color

        @color.setter
        def color(self, value: str):
            self.set_property('_color', value)

        def convert_by(self, axis: IAxisManager) -> Tuple[float, float]:
            return self._find_lower_core(axis, self.range.minimum), self._find_upper_core(axis, self.range.maximum)

        def _find_lower_core(self, axis: IAxisManager, value: float) -> float:
            lo, hi = 0.0, 1e9
            while hi - lo > 1e-6:
                mid = (lo + hi) / 2.0
                if axis.translate_to_axis_value(mid) <= value:
                    lo = mid
                else:
                    hi = mid
            return lo

        def _find_upper_core(self, axis: IAxisManager, value: float) -> float:
            lo, hi = 0.0, 1e9
            while hi - lo > 1e-6:
                mid = (lo + hi) / 2.0
                if axis.translate_to_axis_value(mid) >= value:
                    hi = mid
                else:
                    lo = mid
            return hi
    