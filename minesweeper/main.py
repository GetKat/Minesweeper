import pygame as pg
import os
import sys

from field import Field
from minefield import MineField



HEIGHT = 800
WIDTH = 600

FPS = 60

NUM_MINES = 100
MAX_MINAS = (WIDTH // 20) * (HEIGHT // 20)
TOTAL_QUADRADOS = MAX_MINAS

PATH = os.path.dirname(os.path.abspath(__file__))

clock = pg.time.Clock()

# CLICKES DO MOUSE
M_LCLICK = 1
M_RCLICK = 3

FONT_SIZE = 30
pg.font.init()
my_font = pg.font.SysFont('Times new roman', FONT_SIZE)
PERDEU_TEXT = my_font.render("Tu perdeu", False, [126, 126, 126])
GANHOU_TEXT = my_font.render("Tu ganhou", True, [126, 126, 126])

def main():
    # n pode haver mais minas q quadrados
    if(NUM_MINES > MAX_MINAS):
        print("Tem minas demais!")
        sys.exit(-1)
    
    print("path:", PATH)
    # init
    pg.init()
    pg.display.init()

    # configuracao da screen
    screen = pg.display.set_mode([WIDTH, HEIGHT + FONT_SIZE])
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


    # conta os quadrados revelados
    count_revealed = 0
    # conta o numero de minas q faltam (especulando)
    counter = 0
    # conta o numero de bandeiras colocadas pelo usuario
    count_flags = 0

    perdeu = False
    won = False
    while True:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if(event.type == pg.KEYDOWN):
                if(event.key == pg.K_F2):
                    # def reset()
                    sprites.empty()
                    mine_field = MineField(WIDTH, HEIGHT)
                    sprites.add(mine_field.fields)
                    mine_field.get_mines(NUM_MINES)
                    mine_field.get_numbers()
                    count_revealed = 0
                    perdeu = False
                    won = False
                if(event.key == pg.K_F9):
                    mine_field.toggle_theme()
                if(event.key == pg.K_F1):
                    perdeu = True
            # quando clicka num quadrado
            if(event.type == pg.MOUSEBUTTONDOWN and not perdeu and not won):
                x, y = event.pos
                # passa por todas as minas procurando a bomba dentro de x, y

                for mina in sprites:
                    if(mina.rect.collidepoint(x, y)):
                        # botao direito
                        if(event.button == M_RCLICK):
                            mina.on_right_click()
                            # dps de ter clickado virou uma flag, aumenta o num de flags
                            if(mina.hiden == Field.FLAG):
                                count_flags += 1
                            # se dps de ter clickado virou um "?" significa q era flag, diminiu o numero de flags
                            if(mina.hiden == Field.QUESTION):
                                count_flags -= 1

                        # botao esquerdo
                        elif(event.button == M_LCLICK):
                            #mina.on_left_click()
                            if(mina.number == Field.BOMB and mina.hiden == Field.DEFAULT):
                                perdeu = True
                                mine_field.revelar()
                                mina.set_bomb_exploded()
                            else:
                                count_revealed += mine_field.flood_fill(mina)
        screen.fill([255, 255, 255]) 
        
        # so da pra ganhar se liberar todos os quadrados nao-bomba
        if(TOTAL_QUADRADOS - count_revealed == NUM_MINES):
            won = True

        # mostra a quantidade de minas q faltam (especulacao atravez das bandeiras)
        counter = NUM_MINES - count_flags
        text_count = my_font.render(str(counter), True, [200, 0, 0])
        text_rect = text_count.get_rect()
        text_rect.bottom = HEIGHT + FONT_SIZE
        text_rect.right = WIDTH
        screen.blit(text_count, text_rect)


        # ver quando preencher a tela toda toda com bandeira
        if(perdeu):
            # mostra PERDEU_TEXT na tela
            text_rect = PERDEU_TEXT.get_rect()
            text_rect.bottom = HEIGHT + FONT_SIZE
            text_rect.centerx = WIDTH // 2
            screen.blit(PERDEU_TEXT, text_rect)
        elif(won):
            screen.blit(GANHOU_TEXT, [WIDTH // 2 - PERDEU_TEXT.get_width() // 2, HEIGHT])
        sprites.update()
        sprites.draw(screen)

        pg.display.flip()
        clock.tick(30)


if(__name__ == "__main__"): main()
