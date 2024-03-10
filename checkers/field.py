from checkers import constant


class FieldConsole:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.table = self.generate()

    def generate(self):
        field = [
            ["*" if (x == 0 or x == 9) or (y == 0 or y == 9) else constant.EMPTY_CHAR for x in range(10)]
            for y in range(10)
        ]

        for y in range(1, self.y + 1):
            for x in range(1, self.x + 1):
                if (y + x) % 2:
                    if y < 4:
                        field[y][x] = constant.EMPTY_CHECKER_BLACK
                    elif y >= self.y - 2:
                        field[y][x] = constant.EMPTY_CHECKER_WHITE
        return field

    def show_field(self):
        print(' ', '0', '1', '2', '3', '4', '5', '6', '7', '8')
        for y, v in enumerate(constant.VERTICAL_COORDINATES):
            print(v, ' '.join(self.table[y]))

#
# class Field:
#     def __init__(self, x_coord: int, y_coord: int):
#         self.__x_coord = x_coord
#         self.__y_coord = y_coord
#         self.__generate()
#
#     @property
#     def x_coord(self):
#         return self.__x_coord
#
#     @property
#     def y_coord(self):
#         return self.__y_coord
#
#     @property
#     def size(self) -> int:
#         return max(self.x_coord, self.y_coord)
#
#     @classmethod
#     def copy(cls, field_instance):
#         field_copy = cls(field_instance.x_coord, field_instance.y_coord)
#
#         for y in range(field_instance.y_coord):
#             for x in range(field_instance.x_coord):
#                 field_copy.at(x, y).change_type(field_instance.type_at(x, y))
#
#         return field_copy
#
#     def __generate(self):
#         self.__checkers = [[Checker() for x in range(self.x_coord)] for y in range(self.y_coord)]
#
#         for y in range(self.y_coord):
#             for x in range(self.x_coord):
#                 if (y + x) % 2:
#                     if y < 3:
#                         self.__checkers[y][x].change_type(CheckerType.BLACK_REGULAR)
#                     elif y >= self.y_coord - 3:
#                         self.__checkers[y][x].change_type(CheckerType.WHITE_REGULAR)
#
#     def at(self, x: int, y: int):
#         '''Получение шашки на поле по координатам'''
#         return self.__checkers[y][x]
#
#     @x_coord.setter
#     def x_coord(self, value):
#         self.__x_coord = value
#
#     @y_coord.setter
#     def y_coord(self, value):
#         self.__y_coord = value
