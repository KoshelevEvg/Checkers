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

    def get_user_position(self, field_object, char):
        field = field_object.table
        real_x, real_y = 0, 0
        dy = (-1, -1)
        dx = (-1, 1)

        while True:
            new_char = ""
            invalid_turn = 0
            flag, count, attack_coord = self.check_all_turn(field, char)
            self.check_swap_checkers(field)
            user_char = input(f"User {self.name_user} Select checker: ").strip(" ").lower()
            old_y, old_x = tuple(user_char)
            old_x, old_y = int(old_x), constant.VERTICAL_COORDINATES.index(old_y)
            if field[old_y][old_x] == constant.CHECKER_WHITE_QUEEN:
                new_char = constant.CHECKER_WHITE_QUEEN
            elif field[old_y][old_x] == constant.CHECKER_BLACK_QUEEN:
                new_char = constant.CHECKER_BLACK_QUEEN

            cords = input(f"User {self.name_user} Input coordinates: ").lower().strip(" ")
            y, x = tuple(cords)

            if x not in constant.HORIZONTAL_COORDINATES or y not in constant.VERTICAL_COORDINATES:
                print("Not valid coord")
                continue

            real_x, real_y = int(x), constant.VERTICAL_COORDINATES.index(y)
            if field[real_y][real_x] == "*":
                print("Not valid turn")
                continue
            if not flag:
                for k in range(len(dy)):
                    if char == constant.EMPTY_CHECKER_WHITE:
                        if (real_y == old_y + dy[k] and real_x != old_x + dx[k]) \
                                or (real_y != old_y + dy[k] and real_x == old_x + dx[k]) \
                                or (real_y != old_y + dy[k] and real_x != old_x + dx[k]):
                            invalid_turn += 1
                    elif char == constant.EMPTY_CHECKER_BLACK:
                        if (real_y == old_y - dy[k] and real_x != old_x - dx[k]) \
                                or (real_y != old_y - dy[k] and real_x == old_x - dx[k]) \
                                or (real_y != old_y - dy[k] and real_x != old_x - dx[k]):
                            invalid_turn += 1
            if invalid_turn == 2:
                print("Not valid turn")
                continue
            if count > 0:
                if real_x in attack_coord["x"] and real_y in attack_coord["y"]:
                    print("Kill")
                else:
                    print("Need Attack")
                    continue

            if new_char != "":
                self.turn_queen(real_y, real_x, old_y, old_x, field, new_char)

            if field[real_y][real_x] == constant.EMPTY_CHAR:
                field[real_y][real_x] = char
                # if not self.before_turn_white(field, real_x, real_y):
                break
            elif self.action(field, real_x, real_y, old_x, old_y, char):
                print("Need attack")
                if field[old_y][old_x] == char:
                    field[old_y][old_x] = constant.EMPTY_CHAR
                field_object.show_field()
                continue
            else:
                break
        if field[old_y][old_x] == char:
            field[old_y][old_x] = constant.EMPTY_CHAR
        return real_x, real_y

    def check_all_turn(self, field, char):
        check = False
        count = 0
        attack_coord = {
            "y": [],
            "x": []
        }
        for y in range(1, len(field) - 2):
            for x in range(1, len(field) - 2):
                if field[y][x] == char:
                    a, _ = self.check_attack(field, y, x, char, attack_coord)
                    if a != 0:
                        count += a
                    else:
                        continue
        if count > 0:
            check = True
        return check, count, attack_coord

    @staticmethod
    def check_attack(field, y, x, char, attack_coord):
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, -1, 1)
        attack = 0
        for k in range(len(dy)):
            if char == constant.EMPTY_CHECKER_WHITE:
                if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHECKER_BLACK:
                    if field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                        attack += 1
                        attack_coord["y"].append(y + dy[k])
                        attack_coord["x"].append(x + dx[k])
            elif char == constant.EMPTY_CHECKER_BLACK:
                if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHECKER_WHITE:
                    if field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                        attack += 1
                        attack_coord["y"].append(y + dy[k])
                        attack_coord["x"].append(x + dx[k])
        return attack, attack_coord
        #
        # white = {
        #     "x": [],
        #     "y": []
        # }
        # black = {
        #     "x": [],
        #     "y": []
        # }
        # for y in range(1, len(field) - 2):
        #     for x in range(1, len(field) - 2):
        #         if field[y][x] == constant.EMPTY_CHECKER_WHITE:
        #             y_list, x_list = self.before_turn_white(field, x, y, char)
        #             if len(y_list) == 0 and len(x_list) == 0:
        #                 continue
        #             white["y"] += y_list
        #             white["x"] += x_list
        #         elif field[y][x] == constant.EMPTY_CHECKER_BLACK:
        #             y_list, x_list = self.before_turn_black(field, x, y, char)
        #             if len(y_list) == 0 and len(x_list) == 0:
        #                 continue
        #             black["y"] += y_list
        #             black["x"] += x_list
        # if char == constant.EMPTY_CHECKER_WHITE:
        #     if len(white["y"]) == 0 and len(white["x"]) == 0:
        #         return False, [], []
        #     return True, white["y"], white["x"]
        # if char == constant.EMPTY_CHECKER_BLACK:
        #     if len(black["y"]) == 0 and len(black["x"]) == 0:
        #         return False, [], []
        #     return True, black["y"], black["x"]

    def before_turn_white(self, field, real_x, real_y, char):
        dy = (1, 1, -1, -1)
        dx = (-1, 1, -1, 1)
        attack_zone_y = []
        attack_zone_x = []
        for k in range(len(dx)):
            if field[real_y + dy[k]][real_x + dx[k]] == constant.EMPTY_CHECKER_BLACK:
                if self.after_attack(field, real_x, real_y, char):
                    attack_zone_y.append(real_y + dy[k])
                    attack_zone_x.append(real_x + dx[k])
        return attack_zone_y, attack_zone_x

    def before_turn_black(self, field, real_x, real_y, char):
        dy = (1, 1, -1, -1)
        dx = (-1, 1, -1, 1)
        attack_zone_y = []
        attack_zone_x = []
        for k in range(len(dx)):
            if field[real_y + dy[k]][real_x + dx[k]] == constant.EMPTY_CHECKER_WHITE:
                if self.after_attack(field, real_x, real_y, char):
                    attack_zone_y.append(real_y + dy[k])
                    attack_zone_x.append(real_x + dx[k])
        return attack_zone_y, attack_zone_x

    @staticmethod
    def after_attack(field, real_x, real_y, char):
        dy = (-1, 1, -1, 1)
        dx = (-1, -1, 1, 1)
        for k in range(len(dy)):
            if char == constant.EMPTY_CHECKER_WHITE:
                if field[real_y + dy[k]][real_x + dx[k]] == constant.EMPTY_CHECKER_BLACK \
                        and field[real_y + dy[k] * 2][real_x + dx[k] * 2] == constant.EMPTY_CHAR:
                    return True
            else:
                if field[real_y + dy[k]][real_x + dx[k]] == constant.EMPTY_CHECKER_WHITE \
                        and field[real_y + dy[k] * 2][real_x + dx[k] * 2] == constant.EMPTY_CHAR:
                    return True
        return False

    def action(self, field, real_x, real_y, old_x, old_y, char):
        dx = 1 if real_x > old_x else -1
        dy = -1 if real_y < old_y else 1

        if field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK and field[real_y + dy][real_x + dx] != "*" \
                and field[real_y + dy][real_x + dx] == constant.EMPTY_CHAR:
            field[real_y + dy][real_x + dx] = char
            field[real_y][real_x] = constant.EMPTY_CHAR
            flag, _ = self.check_attack(field, real_y + dy, real_x + dx, char, {})
            if flag > 0:
                return True
            else:
                return False
        elif field[real_y][real_x] == constant.EMPTY_CHECKER_WHITE and field[real_y + dy][real_x + dx] != "*" \
                and field[real_y + dy][real_x + dx] == constant.EMPTY_CHAR:
            field[real_y + dy][real_x + dx] = char
            field[real_y][real_x] = constant.EMPTY_CHAR
            flag, _ = self.check_attack(field, real_y + dy, real_x + dx, char, {})
            if flag > 0:
                return True
            else:
                return False
        return False

    @staticmethod
    def check_swap_checkers(field):
        for k in range(1, len(field) - 2):
            if field[1][k] == constant.EMPTY_CHECKER_WHITE:
                field[1][k] = constant.CHECKER_WHITE_QUEEN
        for k in range(1, len(field) - 2):
            if field[8][k] == constant.EMPTY_CHECKER_BLACK:
                field[8][k] = constant.CHECKER_BLACK_QUEEN

    # @staticmethod
    def turn_queen(self, real_y, real_x, old_y, old_x, field, new_char):
        while not self.action(field, real_x, real_y, old_x, old_y, new_char):
            pass
        print("!!!")
