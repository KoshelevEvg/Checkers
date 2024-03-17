from checkers.enums import SideType, CheckerType
from checkers.point import Point

VERTICAL_COORDINATES = ('-', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '-')
HORIZONTAL_COORDINATES = ('1', '2', '3', '4', '5', '6', '7', '8')
EMPTY_CHAR = '-'
EMPTY_CHECKER_WHITE = 'o'
CHECKER_WHITE_QUEEN = 'O'
EMPTY_CHECKER_BLACK = 'x'
CHECKER_BLACK_QUEEN = 'X'
VALUE_EMPTY_CHAR = 1
VALUE_CHECKER_WHITE = 2
VALUE_CHECKER_WHITE_QUEEN = 4
VALUE_CHECKER_BLACK = 3
VALUE_BLACK_QUEEN = 5
AI_TURN = True
USER_TURN = False
DELTA_Y_WHITE = (-2,-2)
DELTA_X_WHITE = (-2, 2)
DELTA_Y_BLACK = ( 2, 2)
DELTA_X_BLACK = (-2, 2)
MOVE_OFFSETS = [
    Point(-1, -1),
    Point( 1, -1),
    Point(-1,  1),
    Point( 1,  1)
]
WHITE_CHECKERS = [CheckerType.EMPTY_CHECKER_WHITE, CheckerType.CHECKER_WHITE_QUEEN]
BLACK_CHECKERS = [CheckerType.EMPTY_CHECKER_BLACK, CheckerType.CHECKER_BLACK_QUEEN]
# Размер поля
X_SIZE = Y_SIZE = 9
# Размер ячейки (в пикселях)
CELL_SIZE = 75
# Ширина рамки (Желательно должна быть чётной)
BORDER_WIDTH = 2 * 2
# Скорость анимации (больше = быстрее)
ANIMATION_SPEED = 4
# Цвета игровой доски
FIELD_COLORS = ['#E7CFA9', '#927456']
# Цвет рамки при наведении на ячейку мышкой
HOVER_BORDER_COLOR = '#54b346'
# Цвет рамки при выделении ячейки
SELECT_BORDER_COLOR = '#944444'
# Цвет кружков возможных ходов
POSIBLE_MOVE_CIRCLE_COLOR = '#944444'


