import pygame as pg, os

path = os.path.dirname(os.path.abspath(__file__))

class Field(pg.sprite.Sprite):
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
    def __init__(self, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)

        # imagem inicial de qualquer campo
        self.image = pg.image.load(path + "\\icons\\field_3D_filled.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = 0
        self.x = x
        self.y = y
        # hiden state:
        # -1 - revealed
        # 0 - default
        # 1 - flag
        # 2 - ?

        # original state is default

        # number of the field:
        # -1 - bomb
        # 0 - 0 mines arround (no image)
        # 1 - 1 mine arround(1)
        # n - n mines arrounds
        self.hiden = Field.DEFAULT
        self.number = Field.EMPTY
    


    def change_color(self):
        colors = {
            0: gray,
            1: red,
            2: green,
            3: blue
        }
        self.image.fill(colors[self.color])
        self.color = (self.color + 1) % 3

    # retorna se o terreno foi revelado ou n
    def get_hiden(self):
        return self.hiden != Field.REVEALED

    def on_right_click(self):
        # can only change right_click state if not revealed
        if(self.hiden == Field.REVEALED):
            return
        
        # increment the state so it can loop throgh
        #  default(0) -> flag(1) -> question(2) -> default(0) -> ...
        self.hiden = (self.hiden + 1) % 3
        
        if(self.hiden == Field.DEFAULT): # default state
            self.image = pg.image.load(path + "\\icons\\field_3D_filled.png")
        elif(self.hiden == Field.FLAG): # flag state
            self.image = pg.image.load(path + "\\icons\\flag_field_filled.png")
        elif(self.hiden == Field.QUESTION): # question_mark state
            self.image = pg.image.load(path + "\\icons\\question_field_filled.png")

    # when field is left-clicked
    def on_left_click(self):
        # cannot change state if its already clicked
        if(self.hiden != Field.DEFAULT): # state 0 == deafult state (hiden)
            return

        # field now is clicked
        self.hiden = Field.REVEALED

        # reveal true self if its a number (0 included)
        if(self.number != Field.BOMB):
            self.image = pg.image.load(path + "\\icons\\field_1p_" + str(self.number) + ".png")
        else: # hint: its a bomb!
            self.image = pg.image.load(path + "\\icons\\bomb_field.png")