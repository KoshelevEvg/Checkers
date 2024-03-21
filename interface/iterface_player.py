from checkers.move import Move


class IPlayer:

    def get_turns(self, field) -> list:
        pass

    def get_turn(self, field, current_pos: Move, char) -> list:
        pass


def get_all_turns(field, player: IPlayer):
    a = player.get_turns(field)
    return a


def get_turn(field, coord: Move, player: IPlayer):
    a = player.get_turn(field, coord)
    return a
