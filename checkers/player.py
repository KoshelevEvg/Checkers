from checkers import constant
from checkers.move import Move
from checkers.rules import Rules
from interface.iterface_player import IPlayer


class Player(IPlayer):

    def __init__(self, name):
        self.name = name
        self.char = self.get_user_char()
        self.win = False

    @staticmethod
    def get_opponent_char(char):
        return constant.EMPTY_CHECKER_WHITE if char == 'x' else constant.EMPTY_CHECKER_BLACK

    # @staticmethod
    def get_user_char(self):
        user_char = input('Select char (x, o): ').strip(' ').lower()
        while user_char not in ('x', 'o'):
            print('Not available char')
            user_char = input('Select char (x, o): ').strip(' ').lower()
        if user_char == 'x':
            self.char = constant.EMPTY_CHECKER_BLACK
            return self.char
        else:
            self.char = constant.EMPTY_CHECKER_WHITE
            return self.char

    def get_turns(self, field):
        turns = []
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, 1, -1)
        for y in range(1, len(field) - 2):
            for x in range(1, len(field) - 2):
                if field[y][x] == constant.EMPTY_CHECKER_WHITE and field[y][x] != constant.EMPTY_CHAR:
                    for k in range(len(dy)):
                        if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHAR:
                            move = Move(0, 0, 0, 0)
                            move.from_y = y
                            move.from_x = x
                            move.to_y = y + dy[k]
                            move.to_x = x + dx[k]
                            turns.append(move)
                        elif field[y + dy[k]][x + dx[k]] != "*" \
                                and field[y + dy[k]][x + dx[k]] == constant.DELTA_X_BLACK:
                            if field[y + dy[k] * 2][x + dx[k] * 2] != "*" \
                                    and field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                                move = Move(0, 0, 0, 0)
                                move.from_y = y
                                move.from_x = x
                                move.to_y = y + dy[k]
                                move.to_x = x + dx[k]
                                turns.append(move)
                elif field[y][x] == constant.EMPTY_CHECKER_BLACK and field[y][x] != constant.EMPTY_CHAR:
                    for k in range(len(dy)):
                        if field[y + dy[k]][x + dx[k]] != "*" and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHAR:
                            move = Move(0, 0, 0, 0)
                            move.from_y = y
                            move.from_x = x
                            move.to_y = y + dy[k]
                            move.to_x = x + dx[k]
                            turns.append(move)
                        elif field[y + dy[k]][x + dx[k]] != "*" \
                                and field[y + dy[k]][x + dx[k]] == constant.EMPTY_CHECKER_WHITE:
                            if field[y + dy[k] * 2][x + dx[k] * 2] != "*" \
                                    and field[y + dy[k] * 2][x + dx[k] * 2] == constant.EMPTY_CHAR:
                                move = Move(0, 0, 0, 0)
                                move.from_y = y
                                move.from_x = x
                                move.to_y = y + dy[k]
                                move.to_x = x + dx[k]
                                turns.append(move)
                elif field[y][x] == constant.CHECKER_BLACK_QUEEN and field[y][x] != constant.EMPTY_CHAR:
                    pass
        return turns

    def get_turn(self, field, current_pos: Move, char):

        turns = [current_pos]
        attack_list = []
        # dx = 1 if current_pos.to_x > current_pos.from_x else -1
        # dy = -1 if current_pos.to_y < current_pos.from_y else 1
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, -1, 1)
        for k in range(len(dy)):
            move = Move(0, 0, 0, 0)
            move.from_y = current_pos.from_y
            move.from_x = current_pos.from_x
            if field[current_pos.from_y][current_pos.from_x] == constant.EMPTY_CHECKER_WHITE \
                    and char == field[current_pos.from_y][current_pos.from_x]:
                if field[current_pos.from_y + dy[k]][current_pos.from_x + dx[k]] == constant.EMPTY_CHAR:
                    move.to_y = current_pos.from_y + dy[k]
                    move.to_x = current_pos.from_x + dx[k]
                    turns.append(move)
                elif field[current_pos.from_y + dy[k]][current_pos.from_x + dx[k]] == constant.EMPTY_CHECKER_BLACK:
                    if field[current_pos.from_y + dy[k] * 2][current_pos.from_x + dx[k] * 2] == constant.EMPTY_CHAR:
                        move.to_y = current_pos.from_y + dy[k]
                        move.to_x = current_pos.from_x + dx[k]
                        turns.append(move)
                        attack_list.append(move)
            elif field[current_pos.from_y][current_pos.from_x] == constant.EMPTY_CHECKER_BLACK \
                    and char == field[current_pos.from_y][current_pos.from_x]:
                if field[current_pos.from_y + dy[k]][current_pos.from_x + dx[k]] == constant.EMPTY_CHAR:
                    move.to_y = current_pos.from_y + dy[k]
                    move.to_x = current_pos.from_x + dx[k]
                    turns.append(move)
                elif field[current_pos.from_y + dy[k]][current_pos.from_x + dx[k]] == constant.EMPTY_CHECKER_WHITE:
                    if field[current_pos.from_y + dy[k] * 2][current_pos.from_x + dx[k] * 2] == constant.EMPTY_CHAR:
                        move.to_y = current_pos.from_y + dy[k]
                        move.to_x = current_pos.from_x + dx[k]
                        turns.append(move)
                        attack_list.append(move)
        return turns, attack_list

    # def input_coord(self, field_object):
    #     move = Move(0, 0, 0, 0)
    #     user_char = input(f"User {self.name} Select checker: ").strip(" ").lower()
    #     move.from_y, move.from_x = tuple(user_char)
    #     move.from_x, move.from_y = int(move.from_x), constant.VERTICAL_COORDINATES.index(move.from_y)
    #     cords = input(f"User {self.name} Input coordinates: ").lower().strip(" ")
    #     y, x = tuple(cords)
    #     if self.char == constant.EMPTY_CHECKER_BLACK \
    #             and field_object[move.from_y][move.from_x] == constant.CHECKER_BLACK_QUEEN:
    #         self.char = constant.CHECKER_BLACK_QUEEN
    #     elif self.char == constant.EMPTY_CHECKER_WHITE \
    #             and field_object[move.from_y][move.from_x] == constant.CHECKER_WHITE_QUEEN:
    #         self.char = constant.CHECKER_WHITE_QUEEN
    #
    #     while True:
    #         if self.char != field_object[move.from_y][move.from_x] \
    #                 or x not in constant.HORIZONTAL_COORDINATES \
    #                 or y not in constant.VERTICAL_COORDINATES:
    #             print("Not valid checkers")
    #             user_char = input(f"User {self.name} Select checker: ").strip(" ").lower()
    #             move.from_y, move.from_x = tuple(user_char)
    #             move.from_x, move.from_y = int(move.from_x), constant.VERTICAL_COORDINATES.index(move.from_y)
    #             cords = input(f"User {self.name} Input coordinates: ").lower().strip(" ")
    #             y, x = tuple(cords)
    #             continue
    #         else:
    #             break
    #     move.to_x, move.to_y = int(x), constant.VERTICAL_COORDINATES.index(y)
    #     return move
    #
    # def insert_position(self, field_object):
    #     rule = Rules()
    #     # flag_queen = True
    #     move_user = self.input_coord(field_object)
    #     if field_object[move_user.from_y][move_user.from_x] == constant.CHECKER_BLACK_QUEEN \
    #             or field_object[move_user.from_y][move_user.from_x] == constant.CHECKER_WHITE_QUEEN:
    #         list_turn_queen, list_attack_turn_queen = self.turns_queen(field_object, move_user)
    #         flag_queen = rule.check_move_queen(list_turn_queen, list_attack_turn_queen)
    #         while not flag_queen:
    #             print("Don't valid queen turn, retry plz")
    #             move_user = self.input_coord(field_object)
    #             list_turn_queen, list_attack_turn_queen = self.turns_queen(field_object, move_user)
    #             flag_queen = rule.check_move_queen(list_turn_queen, list_attack_turn_queen)
    #             continue
    #         return move_user, list_attack_turn_queen
    #     turns_user, attacks_list = self.get_turn(field_object, move_user, self.char)
    #     attacks_list = self.check_attack(field_object)
    #     flag = rule.check_valid_turn(field_object, turns_user, attacks_list)
    #     while not flag:
    #         print("Don't valid turn, retry plz")
    #         move_user = self.input_coord(field_object)
    #         turns_user, attacks_list = self.get_turn(field_object, move_user, self.char)
    #         flag = rule.check_valid_turn(field_object, turns_user, attacks_list)
    #         continue
    #     return move_user, attacks_list
    def UI_insert_position(self, field_object, move_user):
        rule = Rules()
        # flag_queen = True
        if field_object[move_user.from_y][move_user.from_x] == constant.CHECKER_BLACK_QUEEN \
                or field_object[move_user.from_y][move_user.from_x] == constant.CHECKER_WHITE_QUEEN:
            list_turn_queen, list_attack_turn_queen = self.turns_queen(field_object, move_user)
            flag_queen = rule.check_move_queen(list_turn_queen, list_attack_turn_queen)
            while not flag_queen:
                print("Don't valid queen turn, retry plz")
                # move_user = self.input_coord(field_object)
                list_turn_queen, list_attack_turn_queen = self.turns_queen(field_object, move_user)
                flag_queen = rule.check_move_queen(list_turn_queen, list_attack_turn_queen)
                continue
            return move_user, list_attack_turn_queen
        turns_user, attacks_list = self.get_turn(field_object, move_user, self.char)
        attacks_list = self.check_attack(field_object)
        flag = rule.check_valid_turn(field_object, turns_user, attacks_list)
        while not flag:
            print("Don't valid turn, retry plz")
            # move_user = self.input_coord(field_object)
            turns_user, attacks_list = self.get_turn(field_object, move_user, self.char)
            flag = rule.check_valid_turn(field_object, turns_user, attacks_list)
            continue
        return move_user, attacks_list

    def check_attack(self, field):
        list_attacks = []
        all_turns = self.get_turns(field)
        for k in range(len(all_turns)):
            _, attacks_list = self.get_turn(field, all_turns[k], self.char)
            if len(attacks_list) != 0:
                list_attacks.append(*attacks_list)
        return list_attacks

    def all_turns_queen(self, field):
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, 1, -1)
        for y in range(1, len(field) - 2):
            for x in range(1, len(field) - 2):
                for k in range(len(dy)):
                    for j in range(1, 8):
                        if field[y][x] == constant.CHECKER_WHITE_QUEEN and field[y][x] != constant.EMPTY_CHAR:
                            if 0 <= (y + dy[k] * j) <= 10 or 0 <= (x + dx[k] * j) <= 10:
                                if field[y + dy[k] * j][x + dx[k] * j] != "*" \
                                        and field[y + dy[k] * j][x + dx[k] * j] == constant.EMPTY_CHECKER_BLACK:
                                    pass

    def turns_queen(self, field, coord: Move):
        dy = (-1, -1, 1, 1)
        dx = (-1, 1, 1, -1)
        turns = [coord]
        attack_list, friendly_checkers, enemy_checkers = [], [], []
        if self.char == constant.CHECKER_WHITE_QUEEN:
            friendly_checkers = constant.WHITE_CHECKERS
            enemy_checkers = constant.BLACK_CHECKERS
        elif self.char == constant.CHECKER_BLACK_QUEEN:
            friendly_checkers = constant.BLACK_CHECKERS
            enemy_checkers = constant.WHITE_CHECKERS
        for k in range(len(dy)):
            for j in range(1, 8):
                move = Move(0, 0, 0, 0)
                move.from_y = coord.from_y
                move.from_x = coord.from_x
                if not (0 <= (coord.from_y + dy[k] * j) <= 9 and 0 <= (coord.from_x + dx[k] * j) <= 9):
                    continue
                if field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                        and field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] == constant.EMPTY_CHAR:
                    move.to_y = coord.from_y + dy[k] * j
                    move.to_x = coord.from_x + dx[k] * j
                    turns.append(move)
                elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                        and field[coord.from_y + dy[k] * j][
                    coord.from_x + dx[k] * j] in enemy_checkers:
                    if field[coord.from_y + (dy[k] * (j + 1))][coord.from_x + (dx[k] * (j + 1))] == constant.EMPTY_CHAR:
                        move.to_y = coord.from_y + dy[k] * j
                        move.to_x = coord.from_x + dx[k] * j
                        turns.append(move)
                        attack_list.append(move)
                # elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                #         and field[coord.from_y + dy[k] * j][
                #     coord.from_x + dx[k] * j] in friendly_checkers:
                #     move.to_y = coord.from_y + dy[k] * (j - 1)
                #     move.to_x = coord.from_x + dx[k] * (j - 1)
                #     turns.append(move)
                    # elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                    #         and field[coord.from_y + dy[k] * j][
                    #     coord.from_x + dx[k] * j] == constant.CHECKER_WHITE_QUEEN:
                    #     if field[coord.from_y + (dy[k] * (j + 1))][coord.from_x + (dx[k] * (j + 1))] == constant.EMPTY_CHAR:
                    #         move.to_y = coord.from_y + dy[k] * j
                    #         move.to_x = coord.from_x + dx[k] * j
                    #         turns.append(move)
                    #         attack_list.append(move)
                    # elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                    #         and field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] == constant.EMPTY_CHAR:
                    #     move.to_y = coord.from_y + dy[k] * j
                    #     move.to_x = coord.from_x + dx[k] * j
                    #     turns.append(move)
                    # elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                    #         and field[coord.from_y + dy[k] * j][
                    #     coord.from_x + dx[k] * j] == constant.EMPTY_CHECKER_BLACK:
                    #     if field[coord.from_y + (dy[k] * (j + 1))][coord.from_x + (dx[k] * (j + 1))] == constant.EMPTY_CHAR:
                    #         move.to_y = coord.from_y + dy[k] * j
                    #         move.to_x = coord.from_x + dx[k] * j
                    #         turns.append(move)
                    #         attack_list.append(move)
                    # elif field[coord.from_y + dy[k] * j][coord.from_x + dx[k] * j] != "*" \
                    #         and field[coord.from_y + dy[k] * j][
                    #     coord.from_x + dx[k] * j] == constant.CHECKER_BLACK_QUEEN:
                    #     if field[coord.from_y + (dy[k] * (j + 1))][coord.from_x + (dx[k] * (j + 1))] == constant.EMPTY_CHAR:
                    #         move.to_y = coord.from_y + dy[k] * j
                    #         move.to_x = coord.from_x + dx[k] * j
                    #         turns.append(move)
                    #         attack_list.append(move)
        return turns, attack_list
