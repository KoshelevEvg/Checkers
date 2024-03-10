from checkers import constant
from checkers.move import Move
from interface.iterface_player import AnyPlayer


class Game(AnyPlayer):
    def __init__(self, name_user: str):
        self.name_user = name_user

    def get_turns(self, field):
        move = Move(0, 0, 0, 0)
        turns = []
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, 1, 1)
        for y in range(1, len(field) - 2):
            for x in range(1, len(field) - 2):
                if field[y][x] != constant.EMPTY_CHAR and field[y][x] == constant.EMPTY_CHECKER_WHITE:
                    for k in range(len(dy)):
                        if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHAR:
                            move.to_y = y + dy[k]
                            move.to_x = x + dx[k]
                            turns.append(move)
                        elif field[y + dy[k]][x + dx[k]] != "*" \
                                and field[y + dy[k]][x + dx[k]] == constant.DELTA_X_BLACK:
                            if field[y + dy[k] * 2][x + dx[k] * 2] != "*" \
                                    and field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                                move.to_y = y + dy[k]
                                move.to_x = x + dx[k]
                                turns.append(move)
                elif field[y][x] != constant.EMPTY_CHAR and field[y][x] == constant.EMPTY_CHECKER_BLACK:
                    for k in range(len(dy)):
                        if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHAR:
                            move.to_y = y + dy[k]
                            move.to_x = x + dx[k]
                            turns.append(move)
                        elif field[y + dy[k]][x + dx[k]] != "*" \
                                and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHECKER_WHITE:
                            if field[y + dy[k] * 2][x + dx[k] * 2] != "*" \
                                    and field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                                move.to_y = y + dy[k]
                                move.to_x = x + dx[k]
                                turns.append(move)
        return turns

    def get_turn(self, field, current_pos: Move):
        pass

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

    def input_coord(self):
        move = Move(0, 0, 0, 0)
        user_char = input(f"User {self.name_user} Select checker: ").strip(" ").lower()
        move.from_y, move.from_x = tuple(user_char)
        move.from_x, move.from_y = int(move.from_x), constant.VERTICAL_COORDINATES.index(move.from_y)
        cords = input(f"User {self.name_user} Input coordinates: ").lower().strip(" ")
        y, x = tuple(cords)
        while True:
            if x not in constant.HORIZONTAL_COORDINATES or y not in constant.VERTICAL_COORDINATES:
                print("Not valid coord")
                continue
            else:
                break
        move.to_x, move.to_y = int(x), constant.VERTICAL_COORDINATES.index(y)
        return move

    def get_user_position(self, field_object, char, move: Move):
        field = field_object.table
        # real_x, real_y = 0, 0
        dy = (-1, -1)
        dx = (-1, 1)

        while True:
            new_char = ""
            invalid_turn = 0
            flag, count, attack_coord = self.check_all_turns_attacks(field, char)
            self.check_swap_checkers(field)
            if field[move.from_y][move.from_x] == constant.CHECKER_WHITE_QUEEN:
                new_char = constant.CHECKER_WHITE_QUEEN
            elif field[move.from_y][move.from_x] == constant.CHECKER_BLACK_QUEEN:
                new_char = constant.CHECKER_BLACK_QUEEN
            if field[move.to_y][move.to_x] == "*":
                print("Not valid turn")
                continue
            if not flag:
                for k in range(len(dy)):
                    if char == constant.EMPTY_CHECKER_WHITE:
                        if (move.to_y == move.from_y + dy[k] and move.to_x != move.from_x + dx[k]) \
                                or (move.to_y != move.from_y + dy[k] and move.to_x == move.from_x + dx[k]) \
                                or (move.to_y != move.from_y + dy[k] and move.to_x != move.from_x + dx[k]):
                            invalid_turn += 1
                    elif char == constant.EMPTY_CHECKER_BLACK:
                        if (move.to_y == move.from_y - dy[k] and move.to_x != move.from_x - dx[k]) \
                                or (move.to_y != move.from_y - dy[k] and move.to_x == move.from_x - dx[k]) \
                                or (move.to_y != move.from_y - dy[k] and move.to_x != move.from_x - dx[k]):
                            invalid_turn += 1
            if invalid_turn == 2:
                print("Not valid turn")
                continue
            if count > 0:
                if move.to_x in attack_coord["x"] and move.to_y in attack_coord["y"]:
                    print("Kill")
                else:
                    print("Need Attack")
                    continue

            if new_char != "":
                self.turn_queen(move.to_y, move.to_x, move.from_y, move.from_x, field, new_char)

            if field[move.to_y][move.to_x] == constant.EMPTY_CHAR:
                field[move.to_y][move.to_x] = char
                # if not self.before_turn_white(field, move.to_x, move.to_y):
                break
            elif self.action(field, move.to_x, move.to_y, move.from_x, move.from_y, char):
                print("Need attack")
                if field[move.from_y][move.from_x] == char:
                    field[move.from_y][move.from_x] = constant.EMPTY_CHAR
                field_object.show_field()
                continue
            else:
                break
        if field[move.from_y][move.from_x] == char:
            field[move.from_y][move.from_x] = constant.EMPTY_CHAR
        return move.to_x, move.to_y

    def check_all_turns_attacks(self, field, char):
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
