import pygame as pg, os, sys

from field import Field
from minefield import MineField



HEIGHT = 300
WIDTH = 400

FPS = 15

NUM_MINES = 30

PATH = os.path.dirname(os.path.abspath(__file__))

clock = pg.time.Clock()

# CLICKES DO MOUSE
M_LCLICK = 1
M_RCLICK = 3

pg.font.init()
my_font = pg.font.SysFont('Arial', 30)
text = my_font.render("", True, [126, 126, 126])

def main():
    print("path:", PATH)
    # init
    pg.init()
    pg.display.init()

    # configuracao da screen
    screen = pg.display.set_mode([WIDTH, HEIGHT + 200])
    screen.fill([255, 255, 255])
    pg.display.set_caption("Campo minado")
    pg.display.set_icon(pg.image.load(PATH + "/icons/icon.png"))

    # inicializacao do campo_minado
    mine_field = MineField(WIDTH, HEIGHT)
    mine_field.get_mines(NUM_MINES)
    mine_field.get_numbers()

    # inicializao dos sprites
    sprites = pg.sprite.Group()
    sprites.add(mine_field.fields)



    perdeu = False
    won = False
    while (not perdeu and not won) or True :
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if(perdeu or won):
                continue
            if(event.type == pg.MOUSEBUTTONDOWN):
                x, y = event.pos
                for minas in mine_field.fields:
                    for mina in minas:
                        if(mina.rect.collidepoint(x, y)):
                            if(event.button == M_RCLICK):
                                mina.on_right_click()
                            elif(event.button == M_LCLICK):
                                #mina.on_left_click()
                                if(mina.number == Field.BOMB and mina.hiden == Field.DEFAULT):
                                    perdeu = True
                                    mine_field.revelar()
                                    mina.set_bomb_exploded()
                                mine_field.flood_fill(mina)
            if(event.type == pg.KEYDOWN):
                if(event.key == pg.K_F2):
                    # def reset()
                    sprites.remove(mine_field.fields)
                    mine_field = MineField(WIDTH, HEIGHT)
                    sprites.add(mine_field.fields)
                    mine_field.get_mines(NUM_MINES)
                    mine_field.get_numbers()
                    perdeu = False
                    won = False
                if(event.key == pg.K_F1):
                    perdeu = True
                                      
        if(perdeu):
            white = [255, 255 ,255]
            red = [255, 0 ,0]
            blue = [0, 0, 255]
            global text
            text = my_font.render("Tu perdeu", True, blue)
    
        sprites.update()
        sprites.draw(screen)
        screen.blit(text, [WIDTH // 2 - text.get_width() // 2, HEIGHT])

        pg.display.flip()
        clock.tick(FPS)



if(__name__ == "__main__"): main()
