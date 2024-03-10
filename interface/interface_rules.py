from typing import Protocol


class Rules(Protocol):
    def move(self, current_pos, next_pos):
        pass

    def attack(self, attack_pos):
        pass

    def change_type(self):
        pass
