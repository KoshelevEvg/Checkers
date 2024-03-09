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


        while True:

            flag, y_list, x_list = self.check_attack(field, char)
            user_char = input(f"User {self.name_user} Select checker: ").strip(" ").lower()
            old_y, old_x = tuple(user_char)
            old_x, old_y = int(old_x), constant.VERTICAL_COORDINATES.index(old_y)
            check_turn = self.turn(old_x, old_y, char)

            cords = input(f"User {self.name_user} Input coordinates: ").lower().strip(" ")
            y, x = tuple(cords)

            if x not in constant.HORIZONTAL_COORDINATES or y not in constant.VERTICAL_COORDINATES:
                print("Not valid coord")
                continue

            real_x, real_y = int(x), constant.VERTICAL_COORDINATES.index(y)
            if field[real_y][real_x] == "*":
                print("Not valid turn")
                continue
            if (real_x not in check_turn["x"] and real_y in check_turn["y"]) \
                    or (real_x in check_turn["x"] and real_y not in check_turn["y"]) \
                    or (real_x not in check_turn["x"] and real_y not in check_turn["y"]):
                print("Not valid turn")
                continue

            if flag:
                if real_x in x_list and real_y in y_list:
                    print("Kill")
                else:
                    print("Need Attack")
                    continue

            if field[real_y][real_x] == constant.EMPTY_CHAR:
                field[real_y][real_x] = char
                # if not self.before_turn_white(field, real_x, real_y):
                break
            elif field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK and char == constant.EMPTY_CHECKER_WHITE:
                if real_x - old_x >= 1:
                    if field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK and field[real_y - 1][real_x + 1] != "*":
                        field[real_y - 1][real_x + 1] = char
                        field[real_y][real_x] = constant.EMPTY_CHAR
                        flag, _, _ = self.check_attack(field, char)
                        if flag:
                            print("Need attack")
                            field_object.show_field()
                            continue
                        break
                    else:
                        print("Don't move checker")
                elif real_x - old_x <= -1:
                    if field[real_y][real_x] == constant.EMPTY_CHECKER_BLACK and field[real_y - 1][real_x - 1] != "*":
                        field[real_y - 1][real_x - 1] = char
                        field[real_y][real_x] = constant.EMPTY_CHAR
                        flag, _, _ = self.check_attack(field, char)
                        if flag:
                            print("Need attack")
                            field_object.show_field()
                            continue
                        break
                    else:
                        print("Don't move checker")
            elif field[real_y][real_x] == constant.EMPTY_CHECKER_WHITE and char == constant.EMPTY_CHECKER_BLACK:
                if real_x - old_x >= 1:
                    if field[real_y][real_x] == constant.EMPTY_CHECKER_WHITE and field[real_y + 1][real_x + 1] != "*":
                        field[real_y + 1][real_x + 1] = char
                        field[real_y][real_x] = constant.EMPTY_CHAR
                        flag, _, _ = self.check_attack(field, char)
                        if flag:
                            print("Need attack")
                            field_object.show_field()
                            continue
                        break
                    else:
                        print("Don't move checker")
                elif real_x - old_x <= -1:
                    if field[real_y][real_x] == constant.EMPTY_CHECKER_WHITE and field[real_y + 1][real_x - 1] != "*":
                        field[real_y + 1][real_x - 1] = char
                        field[real_y][real_x] = constant.EMPTY_CHAR
                        flag, _, _ = self.check_attack(field, char)
                        if flag:
                            print("Need attack")
                            field_object.show_field()
                            continue
                        break
                    else:
                        print("Don't move checker")

        if field[old_y][old_x] == char:
            field[old_y][old_x] = constant.EMPTY_CHAR
        return real_x, real_y

    def check_attack(self, field, char):
        white = {
            "x": [],
            "y": []
        }
        black = {
            "x": [],
            "y": []
        }
        for y in range(1, len(field) - 2):
            for x in range(1, len(field) - 2):
                if field[y][x] == constant.EMPTY_CHECKER_WHITE:
                    y_list, x_list = self.before_turn_white(field, x, y, char)
                    if len(y_list) == 0 and len(x_list) == 0:
                        continue
                    white["y"] += y_list
                    white["x"] += x_list
                elif field[y][x] == constant.EMPTY_CHECKER_BLACK:
                    y_list, x_list = self.before_turn_black(field, x, y, char)
                    if len(y_list) == 0 and len(x_list) == 0:
                        continue
                    black["y"] += y_list
                    black["x"] += x_list
        if char == constant.EMPTY_CHECKER_WHITE:
            if len(white["y"]) == 0 and len(white["x"]) == 0:
                return False, [], []
            return True, white["y"], white["x"]
        if char == constant.EMPTY_CHECKER_BLACK:
            if len(black["y"]) == 0 and len(black["x"]) == 0:
                return False, [], []
            return True, black["y"], black["x"]

    def before_turn_white(self, field, real_x, real_y, char):
        dy = (-1, -1)
        dx = (-1, 1)
        attack_zone_y = []
        attack_zone_x = []
        for k in range(len(dx)):
            if field[real_y + dy[k]][real_x + dx[k]] == constant.EMPTY_CHECKER_BLACK:
                if self.after_attack(field, real_x, real_y, char):
                    attack_zone_y.append(real_y + dy[k])
                    attack_zone_x.append(real_x + dx[k])
        return attack_zone_y, attack_zone_x

    def before_turn_black(self, field, real_x, real_y, char):
        dy = (1, 1)
        dx = (-1, 1)
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
        if char == constant.EMPTY_CHECKER_WHITE:
            if field[real_y - 1][real_x - 1] == constant.EMPTY_CHECKER_BLACK and field[real_y - 2][real_x - 2] == constant.EMPTY_CHAR:
                return True
            elif field[real_y - 1][real_x + 1] == constant.EMPTY_CHECKER_BLACK and field[real_y - 2][real_x + 2] == constant.EMPTY_CHAR:
                return True


                # if field[real_y - 2][real_x - 2] == constant.EMPTY_CHAR and:
                #     return True
                # elif field[real_y + constant.DELTA_Y_WHITE[k]][real_x + constant.DELTA_X_WHITE[k]] == "*":

        else:
            if field[real_y + 1][real_x - 1] == constant.EMPTY_CHECKER_WHITE and field[real_y + 2][real_x - 2] == constant.EMPTY_CHAR:
                return True
            elif field[real_y + 1][real_x + 1] == constant.EMPTY_CHECKER_WHITE and field[real_y + 2][real_x + 2] == constant.EMPTY_CHAR:
                return True
        return False

    @staticmethod
    def turn(x, y, char):
        turn_list = {
            "y": [],
            "x": []
        }
        if char == constant.EMPTY_CHECKER_WHITE:
            dy = (-1, -1)
            dx = (-1, 1)
            for k in range(len(dy)):
                turn_list["y"].append(y + dy[k])
                turn_list["x"].append(x + dx[k])
        elif char == constant.EMPTY_CHECKER_BLACK:
            dy = (1, 1)
            dx = (-1, 1)
            for k in range(len(dy)):
                turn_list["y"].append(y + dy[k])
                turn_list["x"].append(x + dx[k])
        return turn_list
