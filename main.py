
from checkers.field import FieldConsole
from checkers.game import Game
from checkers.player import Player


# import os


def main():
    # test(8, 8)

    b = FieldConsole(8, 8)
    # os.system("cls")
    b.show_field()

    user_1 = Player("Player 1")
    user_2 = Player("Player 2")
    Game().start_game(b, user_1, user_2)

    if user_1.win:
        print(f"Player {user_1.name} win")
    elif user_2.win:
        print(f"Player {user_2.name} win")



    # user_2 = Game("Player 2")
    # user_1 = Game("Player 1")
    # user_2 = Game("Player 2")

    # second_user = user_2.get_opponent_char(user_char)
    # while True:
    #     all_turns = get_all_turns(b.table, user_1)
    #
    #     move_user_1 = user_1.input_coord()
    #     # a = get_turn(b.table, move_user_1, user_1)
    #     # a = user_1.get_turns(b.table)
    #
    #     x, y = user_1.get_user_position(b, user_char, move_user_1)
    #     # os.system("cls")
    #     b.show_field()
    #     move_user_2 = user_1.input_coord()
    #     user_2.get_user_position(b, second_user, move_user_2)
    #
    #     # print("!")
    #     # os.system("cls")
    #     b.show_field()
    #     # if is_win(user_char, field):
    #     #     print('you win')
    #     #     break
    #

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
