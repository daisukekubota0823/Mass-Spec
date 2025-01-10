from typing import Optional


    class AxisValue:
        def __init__(self, value: float):
            self.value = value

        def __le__(self, other: "AxisValue") -> bool:
            return self.value <= other.value

        def __ge__(self, other: "AxisValue") -> bool:
            return self.value >= other.value

        def __add__(self, other: float) -> "AxisValue":
            return AxisValue(self.value + other)

        def __sub__(self, other: float) -> "AxisValue":
            return AxisValue(self.value - other)

        def __mul__(self, other: float) -> "AxisValue":
            return AxisValue(self.value * other)

        def __eq__(self, other: "AxisValue") -> bool:
            return self.value == other.value

        def __repr__(self):
            return f"AxisValue({self.value})"


    class AxisRange:
        def __init__(self, minimum: AxisValue, maximum: AxisValue):
            if minimum <= maximum:
                self.minimum = minimum
                self.maximum = maximum
            else:
                self.minimum = AxisValue(0)
                self.maximum = AxisValue(0)

        @property
        def delta(self) -> float:
            return self.maximum.value - self.minimum.value

        def contains(self, value: AxisValue) -> bool:
            return self.minimum <= value <= self.maximum

        def contains_range(self, other: "AxisRange") -> bool:
            return self.contains(other.minimum) and self.contains(other.maximum)

        def intersect(self, other: Optional["AxisRange"]) -> "AxisRange":
            if other is None:
                return self
            return AxisRange(
                AxisValue(max(self.minimum.value, other.minimum.value)),
                AxisValue(min(self.maximum.value, other.maximum.value))
            )

        def union(self, other: Optional["AxisRange"]) -> "AxisRange":
            if other is None:
                return self
            return AxisRange(
                AxisValue(min(self.minimum.value, other.minimum.value)),
                AxisValue(max(self.maximum.value, other.maximum.value))
            )

        @staticmethod
        def union_ranges(lhs: Optional["AxisRange"], rhs: Optional["AxisRange"]) -> Optional["AxisRange"]:
            if lhs is None:
                return rhs
            return lhs.union(rhs)

        def __add__(self, value: AxisValue) -> "AxisRange":
            return AxisRange(self.minimum + value.value, self.maximum + value.value)

        def __sub__(self, value: AxisValue) -> "AxisRange":
            return AxisRange(self.minimum - value.value, self.maximum - value.value)

        def __mul__(self, value: float) -> "AxisRange":
            return AxisRange(self.minimum * value, self.maximum * value)

        def __eq__(self, other: "AxisRange") -> bool:
            return self.minimum == other.minimum and self.maximum == other.maximum

        def __str__(self) -> str:
            return f"{self.minimum.value}-{self.maximum.value}"


    class AxisRangeTypeConverter:
        @staticmethod
        def can_convert_from(source_type: type) -> bool:
            return source_type == str

        @staticmethod
        def convert_from(value: str) -> Optional[AxisRange]:
            if not isinstance(value, str):
                return None

            values = value.split(',')

            if len(values) != 2:
                return None

            try:
                min_value = float(values[0].strip())
                max_value = float(values[1].strip())
            except ValueError:
                return None

            return AxisRange(AxisValue(min_value), AxisValue(max_value))

        @staticmethod
        def can_convert_to(destination_type: type) -> bool:
            return destination_type == str

        @staticmethod
        def convert_to(value: "AxisRange", destination_type: type) -> Optional[str]:
            if not isinstance(value, AxisRange):
                return None
            if destination_type != str:
                return None
            return f"{value.minimum.value},{value.maximum.value}"
    