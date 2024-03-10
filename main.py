# This is a sample Python script.
from checkers import constant
from checkers.field import FieldConsole
from checkers.game import Game
# import os


def main():
    # test(8, 8)
    b = FieldConsole(8, 8)
    # os.system("cls")
    b.show_field()
    user_1 = Game("Player 1")
    user_2 = Game("Player 2")
    user_char = user_1.get_user_char()
    second_user = user_2.get_opponent_char(user_char)
    while True:
        x, y = user_1.get_user_position(b, user_char)
        # os.system("cls")
        b.show_field()
        user_2.get_user_position(b, second_user)

        # print("!")
        # os.system("cls")
        b.show_field()
        # if is_win(user_char, field):
        #     print('you win')
        #     break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
