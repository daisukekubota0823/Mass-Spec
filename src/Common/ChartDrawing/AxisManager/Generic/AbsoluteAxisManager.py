from typing import List, Callable, Optional, TypeVar, Generic
import math

T = TypeVar('T')


class AxisRange:
    def __init__(self, minimum: float, maximum: float):
        self.minimum = minimum
        self.maximum = maximum


class AxisValue:
    def __init__(self, value: float):
        self.value = abs(value)


class BaseAxisManager(Generic[T]):
    def __init__(self, range: AxisRange, bounds: Optional[AxisRange] = None, margin: Optional[float] = None):
        self.range = range
        self.bounds = bounds
        self.margin = margin

    def on_range_changed(self):
        pass

    def get_label_ticks(self):
        pass

    def translate_to_axis_value(self, value: float):
        pass


class AbsoluteAxisManager(BaseAxisManager[float]):
    def __init__(self, *args):
        if isinstance(args[0], AxisRange):
            if len(args) == 1:
                super().__init__(args[0])
            elif len(args) == 2 and isinstance(args[1], AxisRange):
                super().__init__(args[0], args[1])
            elif len(args) == 2 and isinstance(args[1], float):
                super().__init__(args[0], margin=args[1])
            elif len(args) == 3:
                super().__init__(args[0], args[2], args[1])
        elif isinstance(args[0], list):
            source = args[0]
            range_ = self.to_range(source)
            if len(args) == 1:
                super().__init__(range_)
            elif len(args) == 2 and isinstance(args[1], AxisRange):
                super().__init__(range_, args[1])
            elif len(args) == 2 and isinstance(args[1], float):
                super().__init__(range_, margin=args[1])
            elif len(args) == 3:
                super().__init__(range_, args[2], args[1])

        self._label_type = "Standard"
        self._label_generator = None

    @property
    def label_type(self):
        return self._label_type

    @label_type.setter
    def label_type(self, value):
        self._label_type = value
        self._label_generator = None  # Reset the label generator when label type changes

    @property
    def label_generator(self):
        if self._label_type == "Order":
            if not isinstance(self._label_generator, OrderLabelGenerator):
                self._label_generator = OrderLabelGenerator()
        elif self._label_type == "Relative":
            if not isinstance(self._label_generator, RelativeLabelGenerator):
                self._label_generator = RelativeLabelGenerator()
        elif self._label_type == "Percent":
            if not isinstance(self._label_generator, PercentLabelGenerator):
                self._label_generator = PercentLabelGenerator()
        else:  # Standard
            if not isinstance(self._label_generator, StandardLabelGenerator):
                self._label_generator = StandardLabelGenerator()
        return self._label_generator

    def on_range_changed(self):
        self.label_ticks = None
        super().on_range_changed()

    def get_label_ticks(self):
        generator = self.label_generator
        initial_range_core = self.coerce_range(self.range, self.bounds)
        ticks, self.unit_label = generator.generate(
            self.range.minimum, self.range.maximum,
            initial_range_core.minimum, initial_range_core.maximum
        )
        return ticks

    def translate_to_axis_value(self, value: float):
        return AxisValue(value)

    @staticmethod
    def build(source: List[T], map_func: Callable[[T], float]):
        return AbsoluteAxisManager(AbsoluteAxisManager.to_range([map_func(item) for item in source]))

    @staticmethod
    def build_with_bounds(source: List[T], map_func: Callable[[T], float], low_bound: float, high_bound: float):
        return AbsoluteAxisManager(
            AbsoluteAxisManager.to_range([map_func(item) for item in source]),
            AxisRange(low_bound, high_bound)
        )

    @staticmethod
    def to_range(source: List[float]):
        if not source:
            return AxisRange(0, 0)
        return AxisRange(min(source), max(source))


# Dummy label generator classes for demonstration
class OrderLabelGenerator:
    def generate(self, min_val, max_val, initial_min, initial_max):
        return [], None


class RelativeLabelGenerator:
    def generate(self, min_val, max_val, initial_min, initial_max):
        return [], None


class PercentLabelGenerator:
    def generate(self, min_val, max_val, initial_min, initial_max):
        return [], None


class StandardLabelGenerator:
    def generate(self, min_val, max_val, initial_min, initial_max):
        return [], None
