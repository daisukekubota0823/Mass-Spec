from typing import List, Dict, Optional, Iterable, Any
    from collections import defaultdict


    class AxisValue:
        NaN = float('nan')  # 定数としてNaNを定義

        def __init__(self, value: float):
            self.value = value


    class AxisRange:
        def __init__(self, minimum: float, maximum: float):
            self.Minimum = minimum
            self.Maximum = maximum


    class LabelTickData:
        def __init__(self, label: str, tick_type: str, center: float, width: float, source: Any):
            self.Label = label
            self.TickType = tick_type
            self.Center = center
            self.Width = width
            self.Source = source


    class TickType:
        LongTick = "LongTick"


    class FreezableAxisManager:
        def __init__(self):
            self.InitialRange = None

        def GetLabelTicks(self) -> List[LabelTickData]:
            raise NotImplementedError

        def TranslateToAxisValue(self, value: Any) -> AxisValue:
            raise NotImplementedError


    class CategoryAxisManager(FreezableAxisManager):
        def __init__(self):
            super().__init__()
            self.ItemsSource: Optional[Iterable] = None
            self.DisplayPropertyName: Optional[str] = None
            self.IdentityPropertyName: Optional[str] = None
            self.converter: Dict[Any, AxisValue] = {}
            self.data_type: Optional[type] = None
            self.d_property_reflection: Optional[str] = None
            self.i_property_reflection: Optional[str] = None

        def GetLabelTicks(self) -> List[LabelTickData]:
            result = []

            if self.ItemsSource is None:
                return result

            # ラベル生成関数
            if self.d_property_reflection:
                to_label = lambda o: str(getattr(o, self.d_property_reflection, ""))
            else:
                to_label = lambda o: str(o)

            # キー生成関数
            if self.i_property_reflection:
                to_key = lambda o: getattr(o, self.i_property_reflection, o)
            else:
                to_key = lambda o: o

            for item in self.ItemsSource:
                result.append(LabelTickData(
                    label=to_label(item),
                    tick_type=TickType.LongTick,
                    center=self.converter.get(to_key(item), AxisValue.NaN),
                    width=1.0,
                    source=item
                ))

            return result

        def TranslateToAxisValue(self, value: Any) -> AxisValue:
            return self.converter.get(value, AxisValue.NaN)

        def UpdateConverter(self):
            if self.ItemsSource is None:
                return

            self.converter = {}

            items = list(self.ItemsSource)
            if self.i_property_reflection:
                items = list({getattr(item, self.i_property_reflection, None) for item in items})
            else:
                items = list(set(items))

            cnt = 0.0
            for item in items:
                self.converter[item] = 0.5 + cnt
                cnt += 1

            self.InitialRange = AxisRange(minimum=0.0, maximum=cnt)

        def OnItemsSourceChanged(self, old_value: Optional[Iterable], new_value: Optional[Iterable]):
            if new_value is None:
                return

            self.ItemsSource = new_value
            self.data_type = type(next(iter(new_value), None))

            if self.DisplayPropertyName:
                self.d_property_reflection = self.DisplayPropertyName
            if self.IdentityPropertyName:
                self.i_property_reflection = self.IdentityPropertyName

            self.UpdateConverter()

        def OnDisplayPropertyNameChanged(self, old_value: Optional[str], new_value: Optional[str]):
            self.DisplayPropertyName = new_value
            if self.data_type:
                self.d_property_reflection = new_value

        def OnIdentityPropertyNameChanged(self, old_value: Optional[str], new_value: Optional[str]):
            self.IdentityPropertyName = new_value
            if self.data_type:
                self.i_property_reflection = new_value
            self.UpdateConverter()
    