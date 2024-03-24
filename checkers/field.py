from checkers.checker import Checker
from checkers.enums import CheckerType


class FieldConsole:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.__generate()

    def type_at(self, x: int, y: int):
        """Получение типа шашки на поле по координатам"""
        return self.__checkers[y][x].type

    def at(self, x: int, y: int):
        """Получение шашки на поле по координатам"""
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        """Определяет лежит ли точка в пределах поля"""
        return 1 <= x < self.x + 1 and 1 <= y < self.y + 1

    def __generate(self):
        self.__checkers = [[Checker() for x in range(10)]
                           for y in range(10)]

        for y in range(1, self.y + 1):
            for x in range(1, self.x + 1):
                if (y + x) % 2:
                    if y < 4:
                        self.__checkers[y][x].change_type(CheckerType.EMPTY_CHECKER_BLACK)
                    elif y >= self.y - 2:
                        self.__checkers[y][x].change_type(CheckerType.EMPTY_CHECKER_WHITE
                                                          )

        for i in range(0, 10):
            self.__checkers[0][i].change_type(CheckerType.NOT_VALID)
            self.__checkers[i][0].change_type(CheckerType.NOT_VALID)
            self.__checkers[i][9].change_type(CheckerType.NOT_VALID)
            self.__checkers[9][i].change_type(CheckerType.NOT_VALID)
