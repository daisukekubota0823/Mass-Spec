import math
    from typing import List, Tuple


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
        def get_long_interval(self, delta: float) -> float:
            """Determine the long interval based on the given delta."""
            order = math.pow(10, math.floor(math.log10(delta)))
            if delta / order > 2:
                return order
            else:
                return order / 2

        def get_short_interval(self, delta: float, long_interval: float) -> float:
            """Determine the short interval based on the delta and long interval."""
            if delta / long_interval >= 5:
                return long_interval * 0.5
            elif delta / long_interval >= 2:
                return long_interval * 0.25
            else:
                return long_interval * 0.1

        def get_exponent(self, value: float) -> int:
            """Get the exponent of a number."""
            return math.floor(math.log10(value))

        def get_long_ticks(self, lo: float, hi: float, interval: float, factor: float, format_: str) -> List[LabelTickData]:
            """Generate long ticks."""
            result = []
            i = math.ceil(lo / interval)
            while i * interval <= hi:
                value = i * interval
                result.append(LabelTickData(
                    label=f"{value * factor:{format_}}",
                    tick_type=TickType.LongTick,
                    center=value,
                    width=interval,
                    source=value * factor
                ))
                i += 1
            return result

        def get_short_ticks(self, lo: float, hi: float, interval: float, factor: float, format_: str) -> List[LabelTickData]:
            """Generate short ticks."""
            result = []
            i = math.ceil(lo / interval)
            while i * interval <= hi:
                value = i * interval
                result.append(LabelTickData(
                    label=f"{value * factor:{format_}}",
                    tick_type=TickType.ShortTick,
                    center=value,
                    width=0,
                    source=value * factor
                ))
                i += 1
            return result


    class StandardLabelGenerator(LabelGeneratorBase):
        def generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            if low > high:
                return [], ""
            if math.isinf(low) or math.isinf(high) or math.isnan(low) or math.isnan(high):
                return [], ""

            result = []
            long_interval = self.get_long_interval(high - low)

            if long_interval == 0:
                return result, ""

            exp = self.get_exponent(max(abs(high), abs(low)))
            if exp > 3:
                format_ = "0.00e0"
            elif exp < -2:
                format_ = "0.0e0"
            elif long_interval >= 1:
                format_ = ".0f"
            else:
                format_ = ".3f"

            # Add long ticks
            result.extend(self.get_long_ticks(low, high, long_interval, 1, format_))

            short_tick_interval = self.get_short_interval(high - low, long_interval)
            if short_tick_interval == 0:
                return result, ""

            # Add short ticks
            result.extend(self.get_short_ticks(low, high, short_tick_interval, 1, format_))

            return result, ""
    