from enum import Enum
    from typing import List, Any, Iterable, Optional


    class TickType(Enum):
        LongTick = "LongTick"
        ShortTick = "ShortTick"


    class LabelTickData:
        def __init__(self, label: str, tick_type: TickType, center: float, width: float, source: Any):
            self.label = label
            self.tick_type = tick_type
            self.center = center
            self.width = width
            self.source = source


    class AxisRange:
        def __init__(self, minimum: float, maximum: float):
            self.minimum = minimum
            self.maximum = maximum


    class AxisValue:
        def __init__(self, value: float):
            self.value = value


    class IAxisManager:
        def __init__(self):
            self.range_changed = []
            self.initial_range_changed = []
            self.axis_value_mapping_changed = []

        @property
        def range(self) -> AxisRange:
            raise NotImplementedError

        def translate_to_axis_value(self, value: Any) -> AxisValue:
            raise NotImplementedError

        def translate_to_render_point(self, value: AxisValue, is_flipped: bool, drawable_length: float) -> float:
            raise NotImplementedError

        def translate_to_render_points(self, values: Iterable[Any], is_flipped: bool, drawable_length: float) -> List[float]:
            raise NotImplementedError

        def translate_from_render_point(self, value: float, is_flipped: bool, drawable_length: float) -> AxisValue:
            raise NotImplementedError

        def contains(self, value: AxisValue) -> bool:
            raise NotImplementedError

        def contains_current(self, value: AxisValue) -> bool:
            raise NotImplementedError

        def focus(self, range_: AxisRange):
            raise NotImplementedError

        def reset(self):
            raise NotImplementedError

        def recalculate(self, drawable_length: float):
            raise NotImplementedError

        def get_label_ticks(self) -> List[LabelTickData]:
            raise NotImplementedError


    class IAxisManagerT(IAxisManager):
        def translate_to_axis_value(self, value: Any) -> AxisValue:
            raise NotImplementedError

        def translate_to_render_points(self, values: Iterable[Any], is_flipped: bool, drawable_length: float) -> List[float]:
            raise NotImplementedError


    class AxisManager:
        @staticmethod
        def translate_to_render_point(axis: IAxisManager, value: Any, is_flipped: bool, drawable_length: float) -> float:
            axis_value = axis.translate_to_axis_value(value)
            return axis.translate_to_render_point(axis_value, is_flipped, drawable_length)

        @staticmethod
        def translate_to_render_point_t(axis: IAxisManagerT, value: Any, is_flipped: bool, drawable_length: float) -> float:
            axis_value = axis.translate_to_axis_value(value)
            return axis.translate_to_render_point(axis_value, is_flipped, drawable_length)

        @staticmethod
        def contains(axis: IAxisManager, range_: AxisRange) -> bool:
            return axis.contains(AxisValue(range_.minimum)) and axis.contains(AxisValue(range_.maximum))

        @staticmethod
        def contains_value(axis: IAxisManager, value: Any) -> bool:
            axis_value = axis.translate_to_axis_value(value)
            return axis.contains(axis_value)

        @staticmethod
        def contains_value_t(axis: IAxisManagerT, value: Any) -> bool:
            axis_value = axis.translate_to_axis_value(value)
            return axis.contains(axis_value)

        @staticmethod
        def focus(axis: IAxisManager, low: Any, high: Any):
            low_value = axis.translate_to_axis_value(low)
            high_value = axis.translate_to_axis_value(high)
            axis.focus(AxisRange(low_value.value, high_value.value))

        @staticmethod
        def focus_t(axis: IAxisManagerT, low: Any, high: Any):
            low_value = axis.translate_to_axis_value(low)
            high_value = axis.translate_to_axis_value(high)
            axis.focus(AxisRange(low_value.value, high_value.value))
    