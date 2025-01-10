import math
    from typing import List, Optional


    class AxisValue:
        def __init__(self, value: float):
            self.value = value


    class AxisRange:
        def __init__(self, minimum: float, maximum: float):
            self.Minimum = minimum
            self.Maximum = maximum


    class ChartMargin:
        def __init__(self, left: float = 0.0, right: float = 0.0):
            self.Left = left
            self.Right = right


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


    class FreezableAxisManager:
        def __init__(self):
            self.InitialRange = AxisRange(0, 1)

        def GetLabelTicks(self) -> List[LabelTickData]:
            raise NotImplementedError


    class ContinuousAxisManager(FreezableAxisManager):
        def __init__(self):
            super().__init__()
            self.MinValue: Optional[float] = None
            self.MaxValue: Optional[float] = None
            self.ChartMargin = ChartMargin(0.0, 0.0)
            self.Range = self.InitialRange

        def CoerceInitialRange(self):
            min_value = self.MinValue if self.MinValue is not None else 0.0
            max_value = self.MaxValue if self.MaxValue is not None else 1.0

            if min_value == max_value:
                min_value -= 0.5
                max_value += 0.5

            margin = self.ChartMargin
            self.InitialRange = AxisRange(
                minimum=min_value - ((max_value - min_value) * margin.Left),
                maximum=max_value + ((max_value - min_value) * margin.Right)
            )

        def GetLabelTicks(self) -> List[LabelTickData]:
            result = []

            if self.MinValue is None or self.MaxValue is None or self.MinValue >= self.MaxValue:
                return result

            min_value = self.MinValue
            max_value = self.MaxValue

            if math.isnan(min_value) or math.isnan(max_value):
                return result

            tick_interval = math.pow(10, math.floor(math.log10(max_value - min_value)))
            if tick_interval == 0:
                return result

            fold = (max_value - min_value) / tick_interval
            if fold <= 2:
                tick_interval /= 2
                fold *= 2

            short_tick_interval = tick_interval * (0.5 if fold >= 5 else 0.25 if fold >= 2 else 0.1)

            exp = math.floor(math.log10(max_value))
            if exp >= 3:
                label_format = "{:.2e}"
            elif exp < 0:
                label_format = "{:.1e}"
            elif tick_interval >= 1:
                label_format = "{:.0f}"
            else:
                label_format = "{:.3f}"

            # Long ticks
            i = math.ceil(min_value / tick_interval)
            while i * tick_interval <= max_value:
                value = i * tick_interval
                result.append(LabelTickData(
                    label=label_format.format(value),
                    tick_type=TickType.LongTick,
                    center=value,
                    width=tick_interval,
                    source=value
                ))
                i += 1

            # Short ticks
            if short_tick_interval > 0:
                i = math.ceil(min_value / short_tick_interval)
                while i * short_tick_interval <= max_value:
                    value = i * short_tick_interval
                    result.append(LabelTickData(
                        label=label_format.format(value),
                        tick_type=TickType.ShortTick,
                        center=value,
                        width=0,
                        source=value
                    ))
                    i += 1

            return result
    