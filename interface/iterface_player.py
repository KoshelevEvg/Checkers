from checkers.move import Move


class AnyPlayer:

    def get_turns(self, field) -> list:
        pass

    def get_turn(self, field, current_pos: Move) -> list:
        pass


def get_all_turns(field, player: AnyPlayer):
    a = player.get_turns(field)
    return a


# def get_turn(field, coord: Move, player: AnyPlayer):
#     a = player.get_turn(field, coord)
#     return a
