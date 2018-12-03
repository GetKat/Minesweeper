import pygame as pg, sys, os
from field import Field

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

path = os.path.dirname(os.path.abspath(__file__))

def main():
    pg.init()
    pg.display.init()

    screen = pg.display.set_mode([HEIGHT, WIDTH])
    pg.display.set_caption("Campo Minado")
    # icone da janela
    pg.display.set_icon(pg.image.load(path + "\\icons\\icon.png"))
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

if(__name__ == '__main__'): main()