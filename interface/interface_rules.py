from checkers.move import Move


class IRules:
    def move(self, field, current_coord: Move, user):
        pass

    def attack(self, field, attack_pos: Move, user):
        pass

    def check_valid_turn(self, field, possible_moves, attacks_list):
        pass

    def swap_checkers(self, field):
        pass
