import pygame as pg, os, sys

from field import Field
from minefield import MineField

HEIGHT = 400
WIDTH = 600

FPS = 15

PATH = os.path.dirname(os.path.abspath(__file__))

clock = pg.time.Clock()

# CLICKES DO MOUSE
M_LCLICK = 1
M_RCLICK = 3

def main():
    print("path:", PATH)

    # init
    pg.init()
    pg.display.init()

    # configuracao da screen
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    screen.fill([126, 126, 126]) # fill with gray
    pg.display.set_caption("Campo minado")
    pg.display.set_icon(pg.image.load(PATH + "\\icons\\icon.png"))

    # inicializacao do campo_minado
    mine_field = MineField(WIDTH, HEIGHT)
    mine_field.get_mines(400)

    # inicializao dos sprites
    sprites = pg.sprite.Group()
    sprites.add(mine_field.fields)

    while True:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if(event.type == pg.MOUSEBUTTONDOWN):
                x, y = event.pos
                for minas in mine_field.fields:
                    for mina in minas:
                        if(mina.rect.collidepoint(x, y)):
                            if(event.button == M_RCLICK):
                                mina.on_right_click()
                            elif(event.button == M_LCLICK):
                                mina.on_left_click()
        
        sprites.update()
        sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)


if(__name__ == "__main__"): main()