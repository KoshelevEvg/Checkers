from aenum import Enum, auto


class SideType(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(self):
        if self == SideType.WHITE:
            return SideType.BLACK
        elif self == SideType.BLACK:
            return SideType.WHITE
        else:
            raise ValueError()


class CheckerType(Enum):
    NONE = auto()
    WHITE_REGULAR = auto()
    BLACK_REGULAR = auto()
    WHITE_QUEEN = auto()
    BLACK_QUEEN = auto()
