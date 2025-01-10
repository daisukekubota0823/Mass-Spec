from typing import Any


    class AxisValue:
        eps = 1e-9

        NaN = None  # Placeholder for NaN instance

        def __init__(self, value: float):
            self.value = value

        def __lt__(self, other: "AxisValue") -> bool:
            return self.compare_to(other) < 0

        def __gt__(self, other: "AxisValue") -> bool:
            return self.compare_to(other) > 0

        def __le__(self, other: "AxisValue") -> bool:
            return self.compare_to(other) <= 0

        def __ge__(self, other: "AxisValue") -> bool:
            return self.compare_to(other) >= 0

        def compare_to(self, other: "AxisValue") -> int:
            if self.is_nan() and other.is_nan():
                return 0
            if self.is_nan():
                return -1
            if other.is_nan():
                return 1
            if self.value - other.value >= AxisValue.eps:
                return 1
            if other.value - self.value >= AxisValue.eps:
                return -1
            return 0

        def __eq__(self, other: Any) -> bool:
            if not isinstance(other, AxisValue):
                return False
            return self.value == other.value

        def __str__(self) -> str:
            return str(self.value)

        def __hash__(self) -> int:
            return hash(self.value)

        def is_nan(self) -> bool:
            return self.value != self.value  # NaN is not equal to itself


    # Initialize the NaN instance
    AxisValue.NaN = AxisValue(float("nan"))


    class AxisValueTypeConverter:
        @staticmethod
        def can_convert_from(source_type: type) -> bool:
            return source_type == str

        @staticmethod
        def convert_from(value: str) -> AxisValue:
            try:
                return AxisValue(float(value))
            except ValueError:
                return AxisValue.NaN
    