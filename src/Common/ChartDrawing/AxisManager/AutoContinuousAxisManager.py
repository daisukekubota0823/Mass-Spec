from typing import Iterable, Optional
    import math


    class AutoContinuousAxisManager:
        def __init__(self):
            self._items_source = None
            self._value_property_name = None
            self._data_type = None
            self._v_prop = None
            self._min_value = float('inf')
            self._max_value = float('-inf')

        @property
        def ItemsSource(self) -> Optional[Iterable]:
            return self._items_source

        @ItemsSource.setter
        def ItemsSource(self, value: Optional[Iterable]):
            old_value = self._items_source
            self._items_source = value
            self._on_items_source_changed(old_value, value)

        @property
        def ValuePropertyName(self) -> Optional[str]:
            return self._value_property_name

        @ValuePropertyName.setter
        def ValuePropertyName(self, value: Optional[str]):
            old_value = self._value_property_name
            self._value_property_name = value
            self._on_value_property_name_changed(old_value, value)

        @property
        def MinValue(self) -> float:
            return self._min_value

        @MinValue.setter
        def MinValue(self, value: float):
            self._min_value = value

        @property
        def MaxValue(self) -> float:
            return self._max_value

        @MaxValue.setter
        def MaxValue(self, value: float):
            self._max_value = value

        def _set_min_and_max_values(self):
            if not self.ValuePropertyName or not self.ItemsSource or not self._data_type:
                return

            self._v_prop = getattr(self._data_type, self.ValuePropertyName, None)
            if not self._v_prop:
                return

            min_value = float('inf')
            max_value = float('-inf')
            for item in self.ItemsSource:
                if item is None:
                    continue
                try:
                    value = float(getattr(item, self.ValuePropertyName))
                    min_value = min(min_value, value)
                    max_value = max(max_value, value)
                except (ValueError, TypeError, AttributeError):
                    continue

            self.MinValue = min_value
            self.MaxValue = max_value

        def _set_axis_states(self):
            if self.ItemsSource:
                first_item = next(iter(self.ItemsSource), None)
                if first_item is not None:
                    self._data_type = type(first_item)

        def _on_items_source_changed(self, old_value, new_value):
            # Handle collection changes if necessary
            self._set_axis_states()
            self._set_min_and_max_values()

        def _on_value_property_name_changed(self, old_value, new_value):
            self._set_axis_states()
            self._set_min_and_max_values()

        def on_items_source_collection_changed(self):
            self._set_axis_states()
            self._set_min_and_max_values()
    