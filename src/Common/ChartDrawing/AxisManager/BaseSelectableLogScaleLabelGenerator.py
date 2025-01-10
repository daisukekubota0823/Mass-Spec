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


    class LabelGeneratorBase:
        # Base class for label generators (empty for now but can be extended)
        pass


    class ILabelGenerator:
        # Interface for label generators
        def Generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            raise NotImplementedError


    class BaseSelectableLogScaleLabelGenerator(LabelGeneratorBase, ILabelGenerator):
        def __init__(self, base_: int):
            if base_ <= 1:
                raise ValueError("Base must be greater than 1.")
            self.Base = base_

        def Generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            if high <= low or standard_high <= standard_low:
                return [], ""
            if math.isinf(low) or math.isinf(high) or math.isnan(low) or math.isnan(high):
                return [], ""

            result = []
            label = f"log{self.Base}"

            lim_low = math.floor(low)
            lim_high = math.ceil(high)

            result.extend(self._get_int_ticks(
                lim_low, lim_high, 1,
                lambda i, interval: LabelTickData(
                    label=str(self._pow(self.Base, i * interval)),
                    tick_type=TickType.LongTick,
                    center=i * interval,
                    width=interval,
                    source=self._pow(self.Base, i * interval),
                )
            ))
            return result, label

        @staticmethod
        def _pow(base_: int, x: float) -> float:
            return math.pow(base_, x)

        @staticmethod
        def _get_int_ticks(start: float, end: float, interval: float, tick_creator) -> List[LabelTickData]:
            ticks = []
            i = start
            while i <= end:
                ticks.append(tick_creator(i, interval))
                i += interval
            return ticks
    