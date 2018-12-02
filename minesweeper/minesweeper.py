import pygame as pg, sys

black = [0, 0, 0]
white = [255, 255, 255]
gray = [128, 128, 128]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

WIDTH = 400
HEIGHT = 400

"""
MOUSE BUTTONS
1 - left click
2 - middle click
3 - right click
4 - scroll up
5 - scroll down
"""
MOUSE_LEFT = 1
MOUSE_RIGHT = 3

clock = pg.time.Clock()
sprites = pg.sprite.Group() 

def main():
    pg.init()
    pg.display.init()

    screen = pg.display.set_mode([HEIGHT, WIDTH])
    pg.display.set_caption("Campo Minado")
    pg.display.set_icon(pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/icon.png"))
    screen.fill(gray)

    fields = [[Field(x * 20, y * 20) for y in range(20)] for x in range(20)]
    sprites.add(fields)

    while True:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if(event.type == pg.MOUSEMOTION):
                x, y = event.pos
                # print(x, y)
            if(event.type == pg.MOUSEBUTTONDOWN):
                x, y = event.pos
                print('clickou em: ', x, y, '(', event.button, ')')
                if(event.button == MOUSE_RIGHT):
                    for row in fields:
                        for field in row:
                            if(field.rect.collidepoint(x, y)):
                                #field.change_color()
                                field.toggle_right()
                if(event.button == MOUSE_LEFT):
                    for row in fields:
                        for field in row:
                            if(field.rect.collidepoint(x, y)):
                                field.toggle_hiden()


        sprites.update()
        sprites.draw(screen)

        pg.display.flip()
        clock.tick(15)

class Field(pg.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/field_3D_filled.png")
        self.rect = self.image.get_rect()
        """
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        """
        self.rect.x = x
        self.rect.y = y
        self.color = 0
        # hiden state: 0 - regular, 1 - flag, 2 - ?, -1 - revealed
        self.hiden = 0
    
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
        if(self.hiden != -1):
            self.hiden += 1
            if(self.hiden > 2):
                self.hiden = 0
            
            if(self.hiden == 0):
                self.image = pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/field_3D_filled.png")
            elif(self.hiden == 1):
                self.image = pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/flag_field.png")
            elif(self.hiden == 2):
                self.image = pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/question_field.png")

    def toggle_hiden(self):
        if(self.hiden == 0):
            self.hiden = -1
            self.image = pg.image.load("C:/Users/Carlyle/Desktop/pygame/minesweeper/field_1p.png")

if(__name__ == '__main__'): main()