
from checkers.game import Game
from tkinter import Tk, Canvas, PhotoImage
from checkers.constant import X_SIZE, Y_SIZE, CELL_SIZE


def main():
    main_window = Tk()
    main_window.title("Шашки")
    main_window.resizable(False, False)
    main_window.iconphoto(False, PhotoImage(file="icon.png"))

    main_canvas = Canvas(main_window, width=CELL_SIZE * 10, height=CELL_SIZE * 10)
    main_canvas.pack()

    game = Game(main_canvas, X_SIZE, Y_SIZE)
    main_canvas.bind("<Motion>", game.mouse_move)
    main_canvas.bind("<Button-1>", game.mouse_down)

    main_canvas.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
