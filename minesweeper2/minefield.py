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

    def get_mines(self, num_mines):
        count = 0
        while(count < num_mines):
            x, y = random.randint(0, self.width//20 - 1), random.randint(0, self.height//20 - 1)
            if(self.fields[y][x].number != Field.BOMB):
                self.fields[y][x].number = BOMB
                count += 1

    # debugging function
    def print_fields(self):
        for v in self.fields:
            print("[ ", end = '')
            for field in v:
                print("(" + str(field.x) + ", " + str(field.y) + ")", end = ' ')
            print("]")