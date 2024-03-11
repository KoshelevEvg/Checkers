from checkers import constant
from checkers.move import Move
from interface.interface_rules import IRules


class Rules(IRules):

    def __init__(self):
        pass

    def move(self, field, current_coord: Move, user):
        dx = 1 if current_coord.to_x > current_coord.from_x else -1
        dy = -1 if current_coord.to_y < current_coord.from_y else 1

        # if user.char == constant.EMPTY_CHECKER_WHITE:
        #     friendly_checkers = constant.WHITE_CHECKERS
        #     enemy_checkers = constant.BLACK_CHECKERS
        # elif user.char == constant.EMPTY_CHECKER_BLACK:
        #     friendly_checkers = constant.BLACK_CHECKERS
        #     enemy_checkers = constant.WHITE_CHECKERS

        if field[current_coord.from_y][current_coord.from_x] == user.char:
            if field[current_coord.to_y][current_coord.to_x] == constant.EMPTY_CHAR:
                field[current_coord.to_y][current_coord.to_x] = user.char
                field[current_coord.from_y][current_coord.from_x] = constant.EMPTY_CHAR
                return True
            else:
                if self.attack(field, current_coord, user):
                    field[current_coord.from_y][current_coord.from_x] = constant.EMPTY_CHAR
                    field[current_coord.to_y][current_coord.to_x] = constant.EMPTY_CHAR
                    current_coord.from_y = current_coord.to_y + dy
                    current_coord.from_x = current_coord.to_x + dx
                    return True

    def attack(self, field, attack_pos: Move, user):
        dx = 1 if attack_pos.to_x > attack_pos.from_x else -1
        dy = -1 if attack_pos.to_y < attack_pos.from_y else 1

        if field[attack_pos.to_y][attack_pos.to_x] == constant.EMPTY_CHECKER_BLACK:
            if field[attack_pos.to_y + dy][attack_pos.to_x + dx] == constant.EMPTY_CHAR:
                field[attack_pos.to_y + dy][attack_pos.to_x + dx] = user.char
                self.swap_checkers(field)
                return True
        elif field[attack_pos.to_y][attack_pos.to_x] == constant.EMPTY_CHECKER_WHITE:
            if field[attack_pos.to_y + dy][attack_pos.to_x + dx] == constant.EMPTY_CHAR:
                field[attack_pos.to_y + dy][attack_pos.to_x + dx] = user.char
                self.swap_checkers(field)
                return True
        elif field[attack_pos.to_y][attack_pos.to_x] == constant.CHECKER_WHITE_QUEEN:
            if field[attack_pos.to_y + dy][attack_pos.to_x + dx] == constant.EMPTY_CHAR:
                field[attack_pos.to_y + dy][attack_pos.to_x + dx] = user.char
                self.swap_checkers(field)
                return True
        elif field[attack_pos.to_y][attack_pos.to_x] == constant.CHECKER_BLACK_QUEEN:
            if field[attack_pos.to_y + dy][attack_pos.to_x + dx] == constant.EMPTY_CHAR:
                field[attack_pos.to_y + dy][attack_pos.to_x + dx] = user.char
                self.swap_checkers(field)
                return True
        return False

    def check_valid_turn(self, field, possible_moves, attacks_list):
        y_list = []
        x_list = []
        count = 0
        if len(attacks_list) != 0:
            for k in range(len(attacks_list)):
                if possible_moves[0].to_y == attacks_list[k].to_y and possible_moves[0].to_x == attacks_list[k].to_x:
                    count += 1
            if count > 0:
                return True
            else:
                return False
        elif field[possible_moves[0].from_y][possible_moves[0].from_x] == constant.EMPTY_CHECKER_WHITE:
            dy = (-1, -1)
            dx = (-1, 1)
            for k in range(len(dy)):
                y_list.append(possible_moves[0].from_y + dy[k])
                x_list.append(possible_moves[0].from_x + dx[k])
            if possible_moves[0].to_y in y_list and possible_moves[0].to_x in x_list:
                return True

        elif field[possible_moves[0].from_y][possible_moves[0].from_x] == constant.EMPTY_CHECKER_BLACK:
            dy = (1, 1)
            dx = (-1, 1)
            for k in range(len(dy)):
                y_list.append(possible_moves[0].from_y + dy[k])
                x_list.append(possible_moves[0].from_x + dx[k])
            if possible_moves[0].to_y in y_list and possible_moves[0].to_x in x_list:
                return True
        return False

    def swap_checkers(self, field):
        for x in range(1, 8):
            if field[1][x] == constant.EMPTY_CHECKER_WHITE:
                field[1][x] = constant.CHECKER_WHITE_QUEEN
            elif field[8][x] == constant.EMPTY_CHECKER_BLACK:
                field[8][x] = constant.CHECKER_BLACK_QUEEN

    def check_move_queen(self, list_turn, list_attack):
        dx = 1 if list_turn[0].to_x > list_turn[0].from_x else -1
        dy = -1 if list_turn[0].to_y < list_turn[0].from_y else 1
        delta = abs(list_turn[0].to_x - list_turn[0].from_x)
        count = ()
        flag = False
        if len(list_attack) != 0:
            for i in range(len(list_attack)):
                count += (list_attack[i].to_y, list_attack[i].to_x)
            for k in range(delta):
                if list_turn[0].from_y + dy * k in count and list_turn[0].from_x + dx * k in count:
                    flag = True
            if not flag:
                print("Need attack")
                return flag
        # if len(list_attack) != 0:
        #     for k in range(len(list_attack)):
        #         if list_turn[0].to_y == list_attack[k].to_y \
        #                 and list_turn[0].to_x == list_attack[k].to_x:
        #             count += 1
        #     if count > 0:
        #         return True
        for k in range(1, len(list_turn)):
            if list_turn[0].to_y == list_turn[k].to_y \
                    and list_turn[0].to_x == list_turn[k].to_x:
                flag = True
                return flag
        return flag
    def move_queen(self, field, coord: Move, list_attack):
        count = ()
        for i in range(len(list_attack)):
            count += (list_attack[i].to_y, list_attack[i].to_x)
        dx = 1 if coord.to_x > coord.from_x else -1
        dy = -1 if coord.to_y < coord.from_y else 1
        delta = abs(coord.to_x - coord.from_x)
        for k in range(delta):
            if coord.from_y + dy * k in count and coord.from_x + dx * k in count:
                field[coord.from_y + dy * k][coord.from_x + dx * k] = constant.EMPTY_CHAR
        field[coord.to_y][coord.to_x] = field[coord.from_y][coord.from_x]
        field[coord.from_y][coord.from_x] = constant.EMPTY_CHAR

    def is_win(self, field, user):
        count_black = 0
        count_white = 0
        for y in range(1, 8):
            for x in range(1, 8):
                if field[y][x] in constant.BLACK_CHECKERS:
                    count_black += 1
                elif field[y][x] in constant.WHITE_CHECKERS:
                    count_white += 1
        if count_black == 0:
            user.win = True
            return True
        elif count_white == 0:
            user.win = True
            return True
        return False
