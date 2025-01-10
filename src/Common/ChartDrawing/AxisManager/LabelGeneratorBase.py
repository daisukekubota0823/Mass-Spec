import math
    from typing import List, Callable


    class LabelTickData:
        def __init__(self, label: str, tick_type: str, center: float, width: float, source: float):
            self.Label = label
            self.TickType = tick_type
            self.Center = center
            self.Width = width
            self.Source = source


    class TickType:
        LongTick = "LongTick"
        ShortTick = "ShortTick"


    class LabelGeneratorBase:
        @staticmethod
        def get_exponent(x: float) -> float:
            """Calculate the exponent (base-10 logarithm) of a number."""
            return math.floor(math.log10(x))

        @staticmethod
        def get_long_interval(delta: float) -> float:
            """Determine the long interval based on the given delta."""
            order = LabelGeneratorBase.get_order(delta)
            if delta / order > 2:
                return order
            else:
                return order / 2

        @staticmethod
        def get_order(x: float) -> float:
            """Calculate the order of magnitude of a given number."""
            return math.pow(10, LabelGeneratorBase.get_exponent(x))

        @staticmethod
        def get_short_interval(delta: float, long_interval: float) -> float:
            """Determine the short interval based on the delta and long interval."""
            if delta / long_interval >= 5:
                return long_interval * 0.5
            elif delta / long_interval >= 2:
                return long_interval * 0.25
            else:
                return long_interval * 0.1

        def get_real_ticks(self, lo: float, hi: float, interval: float, create: Callable[[float, float], LabelTickData]) -> List[LabelTickData]:
            """Generate real (floating-point) ticks."""
            result = []
            i = lo / interval
            while i * interval <= hi:
                result.append(create(i, interval))
                i += 1
            return result

        def get_int_ticks(self, lo: float, hi: float, interval: float, create: Callable[[float, float], LabelTickData]) -> List[LabelTickData]:
            """Generate integer ticks."""
            result = []
            i = math.ceil(lo / interval)
            while i * interval <= hi:
                result.append(create(i, interval))
                i += 1
            return result

        def get_long_ticks(self, lo: float, hi: float, interval: float, factor: float, format_: str) -> List[LabelTickData]:
            """Generate long ticks."""
            return self.get_int_ticks(
                lo, hi, interval,
                lambda i, interval_: LabelTickData(
                    label=format((i * interval_), format_),
                    tick_type=TickType.LongTick,
                    center=(i * interval_ * factor),
                    width=(interval_ * factor),
                    source=(i * interval_ * factor)
                )
            )

        def get_short_ticks(self, lo: float, hi: float, interval: float, factor: float, format_: str) -> List[LabelTickData]:
            """Generate short ticks."""
            return self.get_int_ticks(
                lo, hi, interval,
                lambda i, interval_: LabelTickData(
                    label=format((i * interval_), format_),
                    tick_type=TickType.ShortTick,
                    center=(i * interval_ * factor),
                    width=0,
                    source=(i * interval_ * factor)
                )
            )
    