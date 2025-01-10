from typing import List, Callable, Optional, TypeVar, Generic, Iterable
from collections.abc import MutableSequence
import math

T = TypeVar('T')
U = TypeVar('U')


class ObservableCollection(MutableSequence):
    """A simple implementation of ObservableCollection-like behavior in Python."""
    def __init__(self, *args):
        self._list = list(*args)
        self._callbacks = []

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        old_value = self._list[index]
        self._list[index] = value
        self._notify("replace", [value], [old_value])

    def __delitem__(self, index):
        old_value = self._list[index]
        del self._list[index]
        self._notify("remove", [], [old_value])

    def __len__(self):
        return len(self._list)

    def insert(self, index, value):
        self._list.insert(index, value)
        self._notify("add", [value], [])

    def append(self, value):
        self._list.append(value)
        self._notify("add", [value], [])

    def extend(self, values):
        self._list.extend(values)
        self._notify("add", values, [])

    def remove(self, value):
        self._list.remove(value)
        self._notify("remove", [], [value])

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        self._callbacks.remove(callback)

    def _notify(self, action, new_items, old_items):
        for callback in self._callbacks:
            callback(self, action, new_items, old_items)


class ContinuousAxisManager(Generic[T]):
    def __init__(self, source: Iterable[T]):
        self.source = source
        self.initial_range = self.calculate_range(source)

    def calculate_range(self, source: Iterable[T]):
        source_list = list(source)
        if not source_list:
            return (0, 0)
        return (min(source_list), max(source_list))

    def update_initial_range(self, source: Iterable[T]):
        self.initial_range = self.calculate_range(source)


class AutoContinuousAxisManager(ContinuousAxisManager[T]):
    EPS = 1e-10

    def __init__(self, source: ObservableCollection[T]):
        super().__init__(source)
        self._source = source
        self._source.add_callback(self.source_changed)

    def source_changed(self, sender, action, new_items, old_items):
        if action in {"reset", "replace"}:
            if self.should_update(new_items, old_items):
                self.update_initial_range(sender)
        elif action == "add":
            if self.should_update_for_new(new_items):
                self.update_initial_range(sender)
        elif action == "remove":
            if self.should_update_for_old(old_items):
                self.update_initial_range(sender)

    def should_update(self, new_values, old_values):
        return self.should_update_for_old(old_values) or self.should_update_for_new(new_values)

    def should_update_for_new(self, new_values):
        if not new_values:
            return True
        new_min = min(new_values)
        new_max = max(new_values)
        if self.initial_range[0] - new_min >= self.EPS:
            return True
        if new_max - self.initial_range[1] >= self.EPS:
            return True
        return False

    def should_update_for_old(self, old_values):
        if not old_values:
            return True
        old_min = min(old_values)
        old_max = max(old_values)
        if abs(old_min - self.initial_range[0]) <= self.EPS:
            return True
        if abs(old_max - self.initial_range[1]) <= self.EPS:
            return True
        return False

    def dispose(self):
        self._source.remove_callback(self.source_changed)


class AutoContinuousAxisManagerWithMapping(ContinuousAxisManager[T]):
    EPS = 1e-10

    def __init__(self, source: ObservableCollection[U], map_func: Callable[[U], T]):
        super().__init__(map(map_func, source))
        self._source = source
        self._map_func = map_func
        self._source.add_callback(self.source_changed)

    def source_changed(self, sender, action, new_items, old_items):
        if action in {"reset", "replace"}:
            if self.should_update(new_items, old_items):
                self.update_initial_range(map(self._map_func, sender))
        elif action == "add":
            if self.should_update_for_new(new_items):
                self.update_initial_range(map(self._map_func, sender))
        elif action == "remove":
            if self.should_update_for_old(old_items):
                self.update_initial_range(map(self._map_func, sender))

    def should_update(self, new_values, old_values):
        return self.should_update_for_old(old_values) or self.should_update_for_new(new_values)

    def should_update_for_new(self, new_values):
        if not new_values:
            return True
        mapped_new_values = list(map(self._map_func, new_values))
        new_min = min(mapped_new_values)
        new_max = max(mapped_new_values)
        if self.initial_range[0] - new_min >= self.EPS:
            return True
        if new_max - self.initial_range[1] >= self.EPS:
            return True
        return False

    def should_update_for_old(self, old_values):
        if not old_values:
            return True
        mapped_old_values = list(map(self._map_func, old_values))
        old_min = min(mapped_old_values)
        old_max = max(mapped_old_values)
        if abs(old_min - self.initial_range[0]) <= self.EPS:
            return True
        if abs(old_max - self.initial_range[1]) <= self.EPS:
            return True
        return False

    def dispose(self):
        self._source.remove_callback(self.source_changed)
