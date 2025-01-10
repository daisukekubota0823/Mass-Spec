from typing import List, Tuple
    import math


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

        def get_int_ticks(self, lo: float, hi: float, interval: float, create):
            """Generate integer ticks."""
            result = []
            i = math.ceil(lo / interval)
            while i * interval <= hi:
                result.append(create(i, interval))
                i += 1
            return result


    class PercentLabelGenerator(LabelGeneratorBase):
        def generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            if high <= low or standard_high <= standard_low:
                return [], ""
            if math.isinf(low) or math.isinf(high) or math.isnan(low) or math.isnan(high):
                return [], ""

            result = []
            label = ""

            delta = high - low
            factor = standard_high - standard_low
            ld = (low - standard_low) / factor
            hd = (high - standard_low) / factor
            delta = (high - low) / factor

            long_interval = self.get_long_interval(delta)
            if long_interval == 0:
                return result, label

            # Add long ticks
            result.extend(
                self.get_int_ticks(ld, hd, long_interval,
                    lambda i, interval: LabelTickData(
                        label=f"{i * interval * 100:.0f}",
                        tick_type=TickType.LongTick,
                        center=(i * interval * factor) + standard_low,
                        width=interval * factor,
                        source=(i * interval * factor) + standard_low
                    )
                )
            )

            short_interval = self.get_short_interval(delta, long_interval)
            if short_interval == 0:
                return result, label

            # Add short ticks
            result.extend(
                self.get_int_ticks(ld, hd, short_interval,
                    lambda i, interval: LabelTickData(
                        label=f"{i * interval * 100:.0f}",
                        tick_type=TickType.ShortTick,
                        center=(i * interval * factor) + standard_low,
                        width=0,
                        source=(i * interval * factor) + standard_low
                    )
                )
            )

            return result, label
    