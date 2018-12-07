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

    # hiden state
    REVEALED = -1
    DEFAULT = 0
    FLAG = 1
    QUESTION = 2

    # themes
    THEME_DEFAULT = 0
    THEME_VAZ = 1
    THEME_LENGHT = 2

    def __init__(self, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)

        # imagem inicial de qualquer campo
        self.image = pg.image.load(path + "/icons/field_3D_filled.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = 0
        self.hiden = Field.DEFAULT
        self.number = Field.EMPTY
        self.theme = Field.THEME_DEFAULT
        self.go_change = False

    def on_right_click(self):
        # can only change right_click state if not revealed
        if(self.hiden == Field.REVEALED):
            return
        
        # increment the state so it can loop throgh
        #  default(0) -> flag(1) -> question(2) -> default(0) -> ...
        self.hiden = (self.hiden + 1) % 3
        self.go_change = True
        
    def update(self):
        if(not self.go_change):
            return
        if(self.hiden == Field.DEFAULT): # default state
            self.image = pg.image.load(path + "/icons/field_3D_filled.png")
        elif(self.hiden == Field.FLAG): # flag state
            self.image = pg.image.load(path + "/icons/flag_field_filled.png")
        elif(self.hiden == Field.QUESTION): # question_mark state
            self.image = pg.image.load(path + "/icons/question_field_filled.png")
        # reveal true self if its a number (0 included)
        elif(self.number != Field.BOMB):
            change_theme = False
            if(self.theme != Field.THEME_DEFAULT):
                new_theme = "_vaz"
                change_theme = True

            self.image = pg.image.load(path + "/icons/field_1p_" + str(self.number) + (new_theme if change_theme else "") + ".png")
        else: # hint: its a bomb!
            self.image = pg.image.load(path + "/icons/bomb_field.png")
        
        self.go_change = False

    # caso vc tenha marcado uma bandeira em um lugar q n era bomba
    def set_wrong_flag(self):
        self.image = pg.image.load(path + "/icons/bomb_field_wrong.png")

    # caso vc tenha clicka em uma bomba :(
    def set_bomb_exploded(self):
        self.image = pg.image.load(path + "/icons/bomb_field_exploded.png")

    # when field is left-clicked
    def on_left_click(self):
        # cannot change state if its already clicked
        if(self.hiden != Field.DEFAULT): # state 0 == deafult state (hiden)
            return

        # field now is clicked
        self.hiden = Field.REVEALED
        self.go_change = True

    def toggle_theme(self):
        self.theme = (self.theme + 1) % Field.THEME_LENGHT
        self.go_change = True