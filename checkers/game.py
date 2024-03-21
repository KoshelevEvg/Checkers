import os

from checkers import constant
from checkers.move import Move
from checkers.player import Player
from checkers.rules import Rules
from interface.iterface_player import IPlayer


class Game(Rules):

    def start_game(self, field, user_1: Player, user_2: Player):
        # user_1_char = user_1.get_user_char()
        # user_2_char = user_2.get_opponent_char(user_1_char)
        self.game(field, user_1, user_2)

    def game(self, field, user_1: Player, user_2: Player):
        field_object = field.table
        while True:
            print("Turn Player 1")
            move_user, list_attacks = user_1.insert_position(field_object)
            if not self.round(field, move_user, user_1, list_attacks):
                break
            self.swap_checkers(field_object)
            os.system('cls')
            field.show_field()
            if self.is_win(field_object, user_1):
                break
            print("Turn Player 2")
            move_user_2, list_attacks = user_2.insert_position(field_object)
            if not self.round(field, move_user_2, user_2, list_attacks):
                break
            self.swap_checkers(field_object)
            os.system('cls')
            field.show_field()
            if self.is_win(field_object, user_2):
                break


    def round(self, field, move_user, user, list_attack):
        if user.char == constant.CHECKER_BLACK_QUEEN or user.char == constant.CHECKER_WHITE_QUEEN:
            self.move_queen(field.table, move_user, list_attack)
            turns_user, attack_user_queen = user.turns_queen(field.table, move_user)
            flag = self.check_move_queen(turns_user, attack_user_queen)
            while len(attack_user_queen) != 0:
                field.show_field()
                print("Need attack")
                move_user = user.insert_position(field.table)
                turns_user, attack_user_queen = user.turns_queen(field.table, move_user)
                flag = self.check_move_queen(turns_user, attack_user_queen)
                self.move_queen(field, move_user, attack_user_queen)
                # a = self.move(field.table, move_user, user)
            # flag = self.check_valid_turn(field.table, turns_user, attack_user)
            return True
        a = self.move(field.table, move_user, user)
        turns_user, attack_user = user.get_turn(field.table, move_user, user.char)
        while len(attack_user) != 0:
            field.show_field()
            print("Need attack")
            move_user = user.insert_position(field.table)
            a = self.move(field.table, move_user, user)
            turns_user, attack_user = user.get_turn(field.table, move_user, user.char)
            # a = self.move(field.table, move_user)
        flag = self.check_valid_turn(field.table, turns_user, attack_user)
        return a
