from abc import ABC, abstractmethod
    from typing import List, Tuple


    class LabelTickData:
        def __init__(self, label: str, tick_type: str, center: float, width: float, source: float):
            self.Label = label
            self.TickType = tick_type
            self.Center = center
            self.Width = width
            self.Source = source


    class ILabelGenerator(ABC):
        @abstractmethod
        def generate(self, low: float, high: float, standard_low: float, standard_high: float) -> Tuple[List[LabelTickData], str]:
            """
            Generate label ticks and a label string for a given range.

            :param low: The lower bound of the range.
            :param high: The upper bound of the range.
            :param standard_low: The standard lower bound.
            :param standard_high: The standard upper bound.
            :return: A tuple containing a list of LabelTickData and a label string.
            """
            pass
    