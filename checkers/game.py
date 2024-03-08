from checkers import constant


class Game:
    def __init__(self, name_user: str):
        self.name_user = name_user

    @staticmethod
    def get_opponent_char(char):
        return constant.EMPTY_CHECKER_WHITE if char == 'x' else constant.EMPTY_CHECKER_BLACK

    @staticmethod
    def get_user_char():
        user_char = input('Select char (x, o): ').strip(' ').lower()
        while user_char not in ('x', 'o'):
            print('Not available char')
            user_char = input('Select char (x, o): ').strip(' ').lower()
        if user_char == 'x':
            return constant.EMPTY_CHECKER_BLACK
        else:
            return constant.EMPTY_CHECKER_WHITE

    def get_user_position(self, field, char):
        real_x, real_y = 0, 0

        while True:
            user_char = input(f"User {self.name_user} Select checker: ").strip(" ").lower()
            old_y, old_x = tuple(user_char)
            old_x, old_y = int(old_x) - 1, constant.VERTICAL_COORDINATES.index(old_y)

            cords = input(f"User {self.name_user} Input coordinates: ").lower().strip(" ")
            y, x = tuple(cords)

            if x not in constant.HORIZONTAL_COORDINATES or y not in constant.VERTICAL_COORDINATES:
                print("Not valid coord")
                continue

            real_x, real_y = int(x) - 1, constant.VERTICAL_COORDINATES.index(y)
            if field[real_y][real_x] == constant.EMPTY_CHAR:
                field[real_y][real_x] = char
                break
            elif field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK and char == constant.EMPTY_CHECKER_WHITE:
                if real_x - old_x >= 1:
                    if field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK:
                        field[real_y - 1][real_x + 1] = char
                        field[real_y][real_x] = constant.EMPTY_CHAR
                        break
                    else:
                        print("Don't move checker")

        if field[old_y][old_x] == char:
            field[old_y][old_x] = constant.EMPTY_CHAR
        return real_x, real_y
