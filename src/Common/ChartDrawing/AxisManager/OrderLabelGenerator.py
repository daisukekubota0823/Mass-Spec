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
        def get_exponent(self, x: float) -> int:
            """Calculate the exponent (base-10 logarithm) of a number."""
            return math.floor(math.log10(x))

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

        def get_long_ticks(self, lo: float, hi: float, interval: float, factor: float, format_: str) -> List[LabelTickData]:
            """Generate long ticks."""
            result = []
            i = math.ceil(lo / interval)
            while i * interval <= hi:
                value = i * interval
                result.append(LabelTickData(
                    label=f"{value * factor:.2f}",
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
                    label=f"{value * factor:.2f}",
                    tick_type=TickType.ShortTick,
                    center=value,
                    width=0,
                    source=value * factor
                ))
                i += 1
            return result


    class OrderLabelGenerator(LabelGeneratorBase):
        def generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            if high <= low:
                return [], ""
            if math.isinf(low) or math.isinf(high) or math.isnan(low) or math.isnan(high):
                return [], ""

            result = []
            label = ""

            delta = high - low
            factor = 1.0
            ld = low
            hd = high
            exp = self.get_exponent(max(abs(low), abs(high)))
            if exp >= 3 or exp <= -2:
                label = f"10^{exp}"
                factor = math.pow(10, exp)
                hd /= factor
                ld /= factor
                delta = (high - low) / factor

            long_interval = self.get_long_interval(delta)
            if long_interval == 0:
                return result, label
            result.extend(self.get_long_ticks(ld, hd, long_interval, factor, "f2"))

            short_interval = self.get_short_interval(delta, long_interval)
            if short_interval == 0:
                return result, label
            result.extend(self.get_short_ticks(ld, hd, short_interval, factor, "f2"))

            return result, label
    