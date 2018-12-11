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
    WRONG_FLAG = -3
    BOMB_EXPLODED = -2
    REVEALED = -1
    DEFAULT = 0
    FLAG = 1
    QUESTION = 2

    # themes
    THEME_DEFAULT = 0
    THEME_VAZ = 1
    THEME_LENGHT = 2

    # IMAGES
    IMG_DEFAULT = pg.image.load(path + "/icons/field_3D_filled.png")
    IMG_FLAG = pg.image.load(path + "/icons/flag_field_filled.png")
    IMG_WRONG_FLAG = pg.image.load(path + "/icons/bomb_field_wrong.png")
    IMG_QUESTION = pg.image.load(path + "/icons/question_field_filled.png")
    IMG_BOMB = pg.image.load(path + "/icons/bomb_field.png")
    IMG_BOMB_EXPLODED = pg.image.load(path + "/icons/bomb_field_exploded.png")

    DEFAULT_NUMBER = []
    for i in range(9):
        img = pg.image.load(path + "/icons/field_1p_" + str(i) + ".png")
        DEFAULT_NUMBER.append(img)
    
    VAZ_NUMBER = []
    for i in range(9):
        img = pg.image.load(path + "/icons/field_1p_" + str(i) + "_vaz.png")
        VAZ_NUMBER.append(img)

    def __init__(self, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)

        # imagem inicial de qualquer campo
        self.image = Field.IMG_DEFAULT
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = 0
        self.hiden = Field.DEFAULT
        self.number = Field.EMPTY
        self.theme = Field.THEME_DEFAULT

    def on_right_click(self):
        # can only change right_click state if not revealed
        if(self.hiden == Field.REVEALED):
            return
        
        # increment the state so it can loop throgh
        #  default(0) -> flag(1) -> question(2) -> default(0) -> ...
        self.hiden = (self.hiden + 1) % 3
        
    def update(self):
        # casos pra cobrir:
        # default (quadrado cheio) -> ok
        # numeros (incluindo 0 (vazio)) -> ok     ""eles sao numeros quando hiden == Field.REVEALED""
        # flag -> ok
        # question -> ok
        # bomb exploded -> ok
        # wrong flag ->

        # default state
        if(self.hiden == Field.DEFAULT): 
            self.image = Field.IMG_DEFAULT

        # flag state
        elif(self.hiden == Field.FLAG): 
            self.image = Field.IMG_FLAG
        
        # question_mark state
        elif(self.hiden == Field.QUESTION): 
            self.image = Field.IMG_QUESTION

        # bomba explodida
        elif(self.hiden == Field.BOMB_EXPLODED):
            self.image = Field.IMG_BOMB_EXPLODED

        # flag errada
        elif(self.hiden == Field.WRONG_FLAG):
            self.image = Field.IMG_WRONG_FLAG

        # reveal itself if its a number (0 included)
        elif(self.number != Field.BOMB):
            # choose theme first
            change_theme = False
            if(self.theme != Field.THEME_DEFAULT):
                new_theme = "_vaz"
                change_theme = True

            self.image = Field.VAZ_NUMBER[self.number] if change_theme else Field.DEFAULT_NUMBER[self.number]
            # self.image = pg.image.load(path + "/icons/field_1p_" + str(self.number) + (new_theme if change_theme else "") + ".png")
        else: # hint: its a bomb!
            self.image = Field.IMG_BOMB
    
    # caso vc tenha marcado uma bandeira em um lugar q n era bomba
    def set_wrong_flag(self):
        self.hiden = Field.WRONG_FLAG

    # caso vc tenha clicka em uma bomba :(
    def set_bomb_exploded(self):
        self.hiden = Field.BOMB_EXPLODED

    # when field is left-clicked
    def on_left_click(self):
        # cannot change state if its already clicked
        if(self.hiden != Field.DEFAULT):
            return

        # field now is clicked
        self.hiden = Field.REVEALED

    def toggle_theme(self):
        # trick to cicle throught theme (1 -> 2 -> 1 -> 2 -> 1 etc...)
        self.theme = (self.theme + 1) % Field.THEME_LENGHT
