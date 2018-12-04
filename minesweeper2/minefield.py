from field import Field
import random

# TODO ver como esconder essa dupla declaracao... sight

# number state
BOMB = -1
EMPTY = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
TEN = 10

# hiden state
REVEALED = -1
DEFAULT = 0
FLAG = 1
QUESTION = 2

class MineField:
    def __init__(self, width, height):
        print("construindo com:", width, height)
        self.fields = [[Field(x, y) for x in range(0, width, 20)] for y in range(0, height, 20)]
        self.width = width
        self.height = height

        self.MAX_MINES = self.width//20 * self.height//20

    def get_mines(self, num_mines):
        count = 0
        if(num_mines > self.MAX_MINES):
            num_mines = self.MAX_MINES
        while(count < num_mines):
            x, y = random.randint(0, self.width//20 - 1), random.randint(0, self.height//20 - 1)
            if(self.fields[y][x].number != Field.BOMB):
                self.fields[y][x].number = BOMB
                count += 1

    def get_numbers(self):
        dir = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
        def ok(x, y):
            return x >= 0 and y >= 0 and x < self.width / 20 and y < self.height / 20

        for fields in self.fields:
            for field in fields:
                if(field.number == Field.BOMB):
                    x = field.rect.x // 20
                    y = field.rect.y // 20
                    for dir_x, dir_y in dir:
                        xx = x + dir_x
                        yy = y + dir_y
                        if(ok(xx, yy) and self.fields[yy][xx].number != Field.BOMB):
                            self.fields[yy][xx].number += 1

    # debugging function
    def print_fields(self):
        for v in self.fields:
            print("[ ", end = '')
            for field in v:
                print("(" + str(field.x) + ", " + str(field.y) + ")", end = ' ')
            print("]")