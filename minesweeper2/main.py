import pygame as pg, os, sys

from field import Field
from minefield import MineField



HEIGHT = 300
WIDTH = 300

FPS = 15

NUM_MINES = 10
MAX_MINAS = (WIDTH // 20) * (HEIGHT // 20)
TOTAL_QUADRADOS = MAX_MINAS

PATH = os.path.dirname(os.path.abspath(__file__))

clock = pg.time.Clock()

# CLICKES DO MOUSE
M_LCLICK = 1
M_RCLICK = 3

pg.font.init()
my_font = pg.font.SysFont('Arial', 30)
PERDEU_TEXT = my_font.render("Tu perdeu", True, [126, 126, 126])
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


    # conta os quadrados revelados
    count_revealed = 0

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
                    sprites.remove(mine_field.fields)
                    mine_field = MineField(WIDTH, HEIGHT)
                    sprites.add(mine_field.fields)
                    mine_field.get_mines(NUM_MINES)
                    mine_field.get_numbers()
                    count_revealed = 0
                    perdeu = False
                    won = False
                if(event.key == pg.K_F1):
                    perdeu = True
            if(perdeu or won):
                continue
            # quando clicka num quadrado
            if(event.type == pg.MOUSEBUTTONDOWN):
                x, y = event.pos
                # passa por todas as minas procurando a bomba dentro de x, y
                for minas in mine_field.fields:
                    for mina in minas:
                        if(mina.rect.collidepoint(x, y)):

                            # botao direito
                            if(event.button == M_RCLICK):
                                mina.on_right_click()

                                # virou flag
                                if(mina.hiden == Field.FLAG):
                                    count_flags += 1
                                    if(mina.number == Field.BOMB):
                                        count_actual_flags += 1
                                # saiu de flag
                                    # lembrando q se vc clicka em um campo bandeira ele vira interrogacao
                                elif(mina.hiden == Field.QUESTION):
                                    count_flags -= 1
                                    if(mina.number == Field.BOMB):
                                        count_actual_flags -= 1

                            # botao esquerdo
                            elif(event.button == M_LCLICK):
                                #mina.on_left_click()
                                if(mina.number == Field.BOMB and mina.hiden == Field.DEFAULT):
                                    perdeu = True
                                    mine_field.revelar()
                                    mina.set_bomb_exploded()
                                count_revealed += mine_field.flood_fill(mina)
         
        # so da pra ganhar se liberar todos os quadrados nao-bomba
        print(TOTAL_QUADRADOS, count_revealed)
        if(TOTAL_QUADRADOS - count_revealed == NUM_MINES):
            won = True

        # ver quando preencher a tela toda toda com bandeira
        if(perdeu):
            # mostra PERDEU_TEXT na tela
            screen.blit(PERDEU_TEXT, [WIDTH // 2 - PERDEU_TEXT.get_width() // 2, HEIGHT])
        elif(won):
            screen.blit(GANHOU_TEXT, [WIDTH // 2 - PERDEU_TEXT.get_width() // 2, HEIGHT])
        else:
            print("jogo em progresso")
            screen.fill([255, 255, 255])
        sprites.update()
        sprites.draw(screen)

        print(count_flags, count_actual_flags)

        pg.display.flip()
        clock.tick(FPS)



if(__name__ == "__main__"): main()
