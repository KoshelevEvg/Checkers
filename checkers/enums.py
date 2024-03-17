class SideType:
    WHITE = 'o'
    BLACK = 'x'

    @staticmethod
    def opposite(side):
        if side == SideType.WHITE:
            return SideType.BLACK
        elif side == SideType.BLACK:
            return SideType.WHITE


class CheckerType:
    NOT_VALID = '*'
    EMPTY_CHAR = '-'
    EMPTY_CHECKER_WHITE = 'o'
    EMPTY_CHECKER_BLACK = 'x'
    CHECKER_WHITE_QUEEN = 'O'
    CHECKER_BLACK_QUEEN = 'X'
