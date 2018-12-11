from field import Field
from queue import Queue
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
    def __init__(self, width, height, num_mines):
        print("construindo com:", width, height)
        self.fields = [[Field(x, y) for x in range(0, width, 20)] for y in range(0, height, 20)]
        self.width = width
        self.height = height

        self.MAX_MINES = self.width//20 * self.height//20
        self.get_mines(num_mines)
        self.get_numbers()
        
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

    def flood_fill(self, mina_origem):
        dir = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
        def ok(x, y):
            return x >= 0 and y >= 0 and x < self.width / 20 and y < self.height / 20

        vis = set()
        vis.add(mina_origem)

        q = Queue()
        q.push(mina_origem)

        while(not q.empty()):
            mina = q.front(); q.pop()
            x = mina.rect.x // 20
            y = mina.rect.y // 20
            mina.on_left_click()
            for dir_x, dir_y in dir:
                xx = x + dir_x
                yy = y + dir_y
                if(ok(xx, yy)):
                    neighbour_mine = self.fields[yy][xx]
                    if(neighbour_mine.number != Field.BOMB and neighbour_mine not in vis and mina.number == Field.EMPTY and mina.hiden != Field.FLAG and mina.hiden != Field.QUESTION):
                        vis.add(neighbour_mine)
                        q.push(neighbour_mine)

    # revela as bombas e as bandeiras erradas
    def revelar(self):
        for field in self.fields:
            for mine in field:
                # se for bomba
                if(mine.number == Field.BOMB):
                    mine.on_left_click()
                # se nao for bomba E tiver uma bandeira
                elif(mine.hiden == Field.FLAG):
                    mine.set_wrong_flag()

    def toggle_theme(self):
        for fields in self.fields:
            for field in fields:
                num = field.number
                if(num != Field.DEFAULT and num != Field.BOMB):
                    field.toggle_theme()