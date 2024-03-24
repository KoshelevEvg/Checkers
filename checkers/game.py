from time import sleep
from tkinter import Canvas, Event, messagebox

from PIL import Image, ImageTk
from checkers.constant import *
from pathlib import Path

from checkers.enums import SideType, CheckerType
from checkers.field import FieldConsole
from checkers.move import Move
from checkers.player import Player
from checkers.point import Point
from checkers.rules import Rules


class Game(Rules, Player):
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int):
        super().__init__()
        self.__field = FieldConsole(8, 8)
        self.__player_side = SideType.WHITE
        self.__player_turn = True
        self.__canvas = canvas
        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()
        self.__init_images()
        self.__draw()
        self.char = EMPTY_CHECKER_WHITE

    def __init_images(self):
        """Инициализация изображений"""
        self.__images = {
            EMPTY_CHECKER_WHITE: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-regular.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            EMPTY_CHECKER_BLACK: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-regular.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            CHECKER_WHITE_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'white-queen.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            CHECKER_BLACK_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'black-queen.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
        }

    def __draw(self):
        """Отрисовка сетки поля и шашек"""
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()

    def __draw_field_grid(self):
        """Отрисовка сетки поля"""
        for y in range(1, 9):
            for x in range(1, 9):
                self.__canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE,
                                               y * CELL_SIZE + CELL_SIZE, fill=FIELD_COLORS[(y + x) % 2], width=0,
                                               tag='boards')

                # Отрисовка рамок у необходимых клеток
                if x == self.__selected_cell.x and y == self.__selected_cell.y:
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2,
                                                   y * CELL_SIZE + BORDER_WIDTH // 2,
                                                   x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   outline=SELECT_BORDER_COLOR,
                                                   width=BORDER_WIDTH,
                                                   tag='border')
                elif x == self.__hovered_cell.x and y == self.__hovered_cell.y:
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2,
                                                   x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   outline=HOVER_BORDER_COLOR, width=BORDER_WIDTH, tag='border')

                # Отрисовка возможных точек перемещения, если есть выбранная ячейка
                if self.__selected_cell:
                    player_moves_list = self.get_moves_list(self.__player_side)
                    for move in player_moves_list:
                        if self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y:
                            self.__canvas.create_oval(move.to_x * CELL_SIZE + CELL_SIZE / 3,
                                                      move.to_y * CELL_SIZE + CELL_SIZE / 3,
                                                      move.to_x * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                                      move.to_y * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                                      fill=POSIBLE_MOVE_CIRCLE_COLOR,
                                                      width=0,
                                                      tag='posible_move_circle')

    def __draw_checkers(self):
        """Отрисовка шашек"""
        for y in range(0, 10):
            for x in range(0, 10):
                # Не отрисовывать пустые ячейки и анимируемую шашку
                # if self.__field.type_at(x, y) != 1 and not (
                #         x == self.__animated_cell.x and y == self.__animated_cell.y):
                if self.__field.type_at(x, y) != CheckerType.NOT_VALID \
                        and not (x == self.__animated_cell.x and y == self.__animated_cell.y):
                    self.__canvas.create_image(x * CELL_SIZE, y * CELL_SIZE,
                                               image=self.__images.get(self.__field.type_at(x, y)),
                                               anchor='nw',
                                               tag='checkers')

    def mouse_move(self, event: Event):
        """Событие перемещения мышки"""
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if x != self.__hovered_cell.x or y != self.__hovered_cell.y:
            self.__hovered_cell = Point(x, y)

            # Если ход игрока, то перерисовать
            if self.__player_turn:
                self.__draw()

    def mouse_down(self, event: Event):
        """Событие нажатия мышки"""
        if not self.__player_turn: return

        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE

        # Если точка не внутри поля
        if not self.__field.is_within(x, y): return

        # Если нажатие по шашке игрока, то выбрать её
        if self.__field.type_at(x, y) in WHITE_CHECKERS or self.__field.type_at(x, y) in BLACK_CHECKERS:
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif self.__player_turn:
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

            # Если нажатие по ячейке, на которую можно походить
            if move in self.get_moves_list(self.__player_side):
                self.handle_player_turn(move)
                self.__player_turn = True
                if self.__player_side == SideType.WHITE:
                    self.__player_side = SideType.BLACK
                elif self.__player_side == SideType.BLACK:
                    self.__player_side = SideType.WHITE

    def handle_player_turn(self, move: Move):

        self.__player_turn = False

        killed = self.handle_move(move)

        required_moves_list = list(
            filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y,
                   self.get_required_moves_list(self.__player_side)))

        # Чек цепочки атаки
        if killed and required_moves_list:
            self.__player_turn = True
            if self.__player_side == SideType.WHITE:
                self.__player_side = SideType.BLACK
            elif self.__player_side == SideType.BLACK:
                self.__player_side = SideType.WHITE

        self.__selected_cell = Point()

    def handle_move(self, move: Move, draw: bool = True) -> bool:

        if draw:
            self.animate_move(move)

        # Изменение типа шашки, если она дошла до края
        if move.to_y == 1 and self.__field.type_at(move.from_x, move.from_y) == CheckerType.EMPTY_CHECKER_WHITE:
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.CHECKER_WHITE_QUEEN)
        elif move.to_y == self.__field.y \
                and self.__field.type_at(move.from_x, move.from_y) == CheckerType.EMPTY_CHECKER_BLACK:
            self.__field.at(move.from_x, move.from_y).change_type(CheckerType.CHECKER_BLACK_QUEEN)

        # Изменение позиции шашки
        self.__field.at(move.to_x, move.to_y).change_type(self.__field.type_at(move.from_x, move.from_y))
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.EMPTY_CHAR)

        # Вектор движения
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        # Удаление шашек
        killed = False
        x, y = move.to_x, move.to_y
        while x != move.from_x or y != move.from_y:
            x += dx
            y += dy
            if self.__field.type_at(x, y) != CheckerType.EMPTY_CHAR:
                self.__field.at(x, y).change_type(CheckerType.EMPTY_CHAR)
                killed = True

        if draw:
            self.__draw()

        self.check_for_game_over()

        return killed

    def check_for_game_over(self):
        """проверка конца игры"""
        game_over = False

        white_checkers_move_list = self.get_moves_list(SideType.WHITE)
        if not white_checkers_move_list:
            # Белые луз
            message = messagebox.showinfo("Конец игры", "Победа черных")
            game_over = True
        black_checkers_move_list = self.get_moves_list(SideType.BLACK)
        if not black_checkers_move_list:
            message = messagebox.showinfo("Конец игры", "Победа белых")
            game_over = True

        if game_over:
            self.__init__(self.__canvas, self.__field.x, self.__field.y)

    def animate_move(self, move: Move):
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        animated_checkers = self.__canvas.create_image(move.from_x * CELL_SIZE, move.from_y * CELL_SIZE,
                                                       image=self.__images.get(
                                                           self.__field.at(move.from_x, move.from_y)),
                                                       anchor="nw",
                                                       tag="animated_checker")

        dx = 1 if move.from_x < move.from_y else -1
        dy = 1 if move.from_y < move.from_x else -1

        for distance in range(abs(move.from_x - move.from_y)):
            for _ in range(100 // ANIMATION_SPEED):
                self.__canvas.move(animated_checkers, ANIMATION_SPEED / 100 * CELL_SIZE * dx,
                                   ANIMATION_SPEED / 100 * CELL_SIZE * dy)
                self.__canvas.update()
                sleep(0.01)

        self.__animated_cell = Point()

    def get_moves_list(self, side: SideType):
        moves_list = self.get_required_moves_list(side)
        if not moves_list:
            moves_list = self.get_optional_moves_list(side)
        return moves_list

    # @staticmethod
    def get_required_moves_list(self, side: SideType):
        moves_list = []

        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
            enemy_checkers = BLACK_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
            enemy_checkers = WHITE_CHECKERS
        else:
            return moves_list

        for y in range(1, 9):
            for x in range(1, 9):

                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(x + offset.x * 2, y + offset.y * 2):
                            continue
                        a = self.__field.type_at(x + offset.x, y + offset.y)
                        if a in enemy_checkers \
                                and self.__field.type_at(x + offset.x * 2, y + offset.y * 2) == CheckerType.EMPTY_CHAR:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))

                # Дамка шеф
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(x + offset.x * 2, y + offset.y * 2):
                            continue

                        has_enemy_checker_on_way = False

                        for shift in range(1, 8):
                            if not self.__field.is_within(x + offset.x * shift, y + offset.y * shift):
                                continue
                            # Если на пути не было вражеской шашки
                            if not has_enemy_checker_on_way:
                                if self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers:
                                    has_enemy_checker_on_way = True
                                    continue
                                elif self.__field.type_at(x + offset.x * shift,
                                                          y + offset.y * shift) in friendly_checkers:
                                    break
                            # Если на пути была вражеская шашка
                            if has_enemy_checker_on_way:
                                if self.__field.type_at(x + offset.x * shift,
                                                        y + offset.y * shift) == CheckerType.EMPTY_CHAR:
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break
        return moves_list

    def get_optional_moves_list(self, side: SideType):
        """Получение списка необязательных ходов"""
        moves_list = []

        if side == SideType.WHITE:
            friendly_checkers = WHITE_CHECKERS
        elif side == SideType.BLACK:
            friendly_checkers = BLACK_CHECKERS
        else:
            return moves_list

        for y in range(1, 9):
            for x in range(1, 9):
                # Для обычной шашки
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]:
                        if not self.__field.is_within(x + offset.x, y + offset.y):
                            continue
                        a = self.__field.type_at(x + offset.x, y + offset.y)
                        if a == CheckerType.EMPTY_CHAR:
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))
                # Дамка сэр
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not self.__field.is_within(x + offset.x, y + offset.y):
                            continue
                        for shift in range(1, 9):
                            if not self.__field.is_within(x + offset.x * shift, y + offset.y * shift):
                                continue
                            if self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == EMPTY_CHAR:
                                moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
        return moves_list
