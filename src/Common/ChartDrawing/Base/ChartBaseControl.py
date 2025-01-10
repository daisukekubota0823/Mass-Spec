from abc import ABC, abstractmethod
from typing import Any, Optional, List


class DependencyProperty:
    """Simulates WPF DependencyProperty behavior."""
    def __init__(self, name, property_type, owner_type, default_value=None, options=None, callback=None):
        self.name = name
        self.property_type = property_type
        self.owner_type = owner_type
        self.default_value = default_value
        self.options = options
        self.callback = callback


class IAxisManager(ABC):
    """Simulates IAxisManager interface."""
    @abstractmethod
    def focus(self, range_value):
        pass

    @property
    @abstractmethod
    def range(self):
        pass


class AxisRange:
    """Simulates AxisRange class."""
    pass


class ChartBaseControl(ABC):
    HorizontalAxisProperty = DependencyProperty(
        "HorizontalAxis", IAxisManager, "ChartBaseControl", default_value=None
    )
    VerticalAxisProperty = DependencyProperty(
        "VerticalAxis", IAxisManager, "ChartBaseControl", default_value=None
    )
    FlippedXProperty = DependencyProperty(
        "FlippedX", bool, "ChartBaseControl", default_value=False
    )
    FlippedYProperty = DependencyProperty(
        "FlippedY", bool, "ChartBaseControl", default_value=True
    )

    def __init__(self):
        self._horizontal_axis: Optional[IAxisManager] = None
        self._vertical_axis: Optional[IAxisManager] = None
        self._flipped_x: bool = False
        self._flipped_y: bool = True
        self.visual_children: List[Any] = []

    @property
    def horizontal_axis(self) -> Optional[IAxisManager]:
        return self._horizontal_axis

    @horizontal_axis.setter
    def horizontal_axis(self, value: IAxisManager):
        old_value = self._horizontal_axis
        self._horizontal_axis = value
        self.on_horizontal_axis_changed(old_value, value)

    def on_horizontal_axis_changed(self, old_value: Optional[IAxisManager], new_value: Optional[IAxisManager]):
        if old_value:
            print("Detach events from old horizontal axis.")
        if new_value:
            print("Attach events to new horizontal axis.")

    @property
    def vertical_axis(self) -> Optional[IAxisManager]:
        return self._vertical_axis

    @vertical_axis.setter
    def vertical_axis(self, value: IAxisManager):
        old_value = self._vertical_axis
        self._vertical_axis = value
        self.on_vertical_axis_changed(old_value, value)

    def on_vertical_axis_changed(self, old_value: Optional[IAxisManager], new_value: Optional[IAxisManager]):
        if old_value:
            print("Detach events from old vertical axis.")
        if new_value:
            print("Attach events to new vertical axis.")

    @property
    def range_x(self) -> Optional[AxisRange]:
        return self.horizontal_axis.range if self.horizontal_axis else None

    @range_x.setter
    def range_x(self, value: AxisRange):
        if self.horizontal_axis:
            self.horizontal_axis.focus(value)

    @property
    def range_y(self) -> Optional[AxisRange]:
        return self.vertical_axis.range if self.vertical_axis else None

    @range_y.setter
    def range_y(self, value: AxisRange):
        if self.vertical_axis:
            self.vertical_axis.focus(value)

    @property
    def flipped_x(self) -> bool:
        return self._flipped_x

    @flipped_x.setter
    def flipped_x(self, value: bool):
        self._flipped_x = value
        self.invalidate_visual()

    @property
    def flipped_y(self) -> bool:
        return self._flipped_y

    @flipped_y.setter
    def flipped_y(self, value: bool):
        self._flipped_y = value
        self.invalidate_visual()

    def invalidate_visual(self):
        print("Invalidate visual called.")

    def on_render(self):
        print("Render logic here.")
        self.update()

    def update(self):
        print("Update chart logic.")

    def on_mouse_left_button_up(self):
        print("Mouse left button released.")

    def on_mouse_right_button_up(self):
        print("Mouse right button released.")

    def on_mouse_wheel(self):
        print("Mouse wheel scrolled.")

    def visual_children_count(self) -> int:
        return len(self.visual_children)

    def get_visual_child(self, index: int) -> Any:
        if index < 0 or index >= len(self.visual_children):
            raise IndexError("Index out of range.")
        return self.visual_children[index]
