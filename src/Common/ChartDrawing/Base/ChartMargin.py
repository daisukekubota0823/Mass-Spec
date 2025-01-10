from typing import Tuple, List, Optional


class ChartMargin:
    def __init__(self, left: float = 0.0, right: Optional[float] = None):
        if right is None:
            right = left
        self.left = left
        self.right = right

    def add(self, lower: float, upper: float) -> Tuple[float, float]:
        delta = upper - lower
        return lower - delta * self.left, upper + delta * self.right

    def remove(self, lower: float, upper: float) -> Tuple[float, float]:
        delta = (upper - lower) / (1 + self.left + self.right)
        x = lower + self.left * delta
        return x, x + delta

    def __str__(self):
        return f"{self.left},{self.right}"


class RelativeMargin:
    def __init__(self, lower: float, upper: Optional[float] = None):
        if upper is None:
            upper = lower
        self.lower = lower
        self.upper = upper

    def add(self, lower: float, upper: float) -> Tuple[float, float]:
        if lower > upper:
            return lower, upper
        delta = upper - lower
        return lower - delta * self.lower, upper + delta * self.upper

    def remove(self, lower: float, upper: float) -> Tuple[float, float]:
        if lower > upper:
            return lower, upper
        delta = (upper - lower) / (1 + self.upper + self.lower)
        return lower + self.lower * delta, upper - self.upper * delta

    def __str__(self):
        return f"{self.lower}*,{self.upper}*"


class ConstantMargin:
    def __init__(self, lower: float, upper: Optional[float] = None):
        if upper is None:
            upper = lower
        self.lower = lower
        self.upper = upper

    def add(self, lower: float, upper: float) -> Tuple[float, float]:
        return lower - self.lower, upper + self.upper

    def remove(self, lower: float, upper: float) -> Tuple[float, float]:
        return lower + self.lower, upper - self.upper

    def __str__(self):
        return f"{self.lower}+,{self.upper}+"


class ChartMarginConverter:
    @staticmethod
    def from_string(value: str) -> Optional[ChartMargin]:
        values = value.split(',')
        if len(values) == 1:
            try:
                left = float(values[0].strip())
                return ChartMargin(left)
            except ValueError:
                return None
        elif len(values) == 2:
            try:
                left = float(values[0].strip())
                right = float(values[1].strip())
                return ChartMargin(left, right)
            except ValueError:
                return None
        return None

    @staticmethod
    def to_string(margin: ChartMargin) -> str:
        return str(margin)


class ChartMargin2Converter:
    @staticmethod
    def from_string(value: str) -> Optional[object]:
        values = value.split(',')
        if len(values) == 0 or len(values) > 2:
            return None

        if all(v.endswith('+') for v in values):
            try:
                left, right = ChartMargin2Converter._parse_margin(
                    [v.strip('+') for v in values]
                )
                return ConstantMargin(left, right)
            except ValueError:
                return None
        elif all(v.endswith('*') for v in values):
            try:
                left, right = ChartMargin2Converter._parse_margin(
                    [v.strip('*') for v in values]
                )
                return RelativeMargin(left, right)
            except ValueError:
                return None
        else:
            try:
                left, right = ChartMargin2Converter._parse_margin(values)
                return RelativeMargin(left, right)
            except ValueError:
                return None

    @staticmethod
    def _parse_margin(values: List[str]) -> Tuple[float, float]:
        if len(values) == 1:
            left = float(values[0].strip())
            return left, left
        elif len(values) == 2:
            left = float(values[0].strip())
            right = float(values[1].strip())
            return left, right
        else:
            raise ValueError("Invalid margin format.")

    @staticmethod
    def to_string(margin: object) -> str:
        return str(margin)
