import pygame as pg, os

path = os.path.dirname(os.path.abspath(__file__))

class Field(pg.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)
        # imagem inicial de qualquer campo
        self.image = pg.image.load(path + "\\icons\\field_3D_filled.png")
        self.rect = self.image.get_rect()
        """
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        """
        self.rect.x = x
        self.rect.y = y
        self.color = 0
        # hiden state:
        # -1 - revealed
        # 0 - default
        # 1 - flag
        # 2 - ?

        # original state is default
        self.hiden = 0

        # number of the field:
        # -1 - bomb
        # 0 - 0 mines arround (no image)
        # 1 - 1 mine arround(1)
        # n - n mines arrounds
        self.number = 0
    
    def change_color(self):
        colors = {
            0: gray,
            1: red,
            2: green,
            3: blue
        }
        self.image.fill(colors[self.color])

        self.color += 1
        if(self.color > 2):
            self.color = 0

    # retorna se o terreno foi revelado ou n
    def get_hiden(self):
        return self.hiden != -1

    def toggle_right(self):
        # can only change right_click state if not revealed
        if(self.hiden == -1):
            return
        
        # increment the state so it can loop throgh
        #  default(0) -> flag(1) -> question(2) -> default(0) -> ...
        self.hiden = (self.hiden + 1) % 3
        
        if(self.hiden == 0): # default state
            self.image = pg.image.load(path + "\\icons\\field_3D_filled.png")
        elif(self.hiden == 1): # flag state
            self.image = pg.image.load(path + "\\icons\\flag_field_filled.png")
        elif(self.hiden == 2): # question_mark state
            self.image = pg.image.load(path + "\\icons\\question_field_filled.png")

    # when field is left-clicked
    def toggle_hiden(self):
        # cannot change state if its already clicked
        if(self.hiden != 0): # state 0 == deafult state (hiden)
            return

        # field now is clicked
        self.hiden = -1

        # reveal true self if its a number (0 included)
        if(self.number != -1):
            self.image = pg.image.load(path + "\\icons\\field_1p_" + str(self.number) + ".png")
        else: # hint: its a bomb!
            self.image = pg.image.load(path + "\\icons\\bomb_field.png")
