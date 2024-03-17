
class Move:

    def __init__(self, from_x, from_y, to_x, to_y):
        self.__from_x = from_x
        self.__from_y = from_y
        self.__to_x = to_x
        self.__to_y = to_y

    @property
    def from_x(self):
        return self.__from_x

    @property
    def from_y(self):
        return self.__from_y

    @property
    def to_x(self):
        return self.__to_x

    @property
    def to_y(self):
        return self.__to_y

    @from_x.setter
    def from_x(self, value):
        self.__from_x = value

    @from_y.setter
    def from_y(self, value):
        self.__from_y = value

    @to_x.setter
    def to_x(self, value):
        self.__to_x = value

    @to_y.setter
    def to_y(self, value):
        self.__to_y = value

    def __str__(self):
        return f'{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}'

    def __repr__(self):
        return f'{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}'

    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.from_x == other.from_x and
                self.from_y == other.from_y and
                self.to_x == other.to_x and
                self.to_y == other.to_y
            )
        return NotImplemented
