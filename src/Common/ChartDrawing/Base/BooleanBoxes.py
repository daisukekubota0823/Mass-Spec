class BooleanBoxes:
    TrueBox = True
    FalseBox = False

    @staticmethod
    def box(value: bool) -> bool:
        return BooleanBoxes.TrueBox if value else BooleanBoxes.FalseBox
