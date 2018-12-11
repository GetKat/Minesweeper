import pygame as pg
import os
import sys

from field import Field
from minefield import MineField

# path para a pasta onde o programa esta rodando... n sei como funciona, pesquisar no stack overflow
PATH = os.path.dirname(os.path.abspath(__file__))

# configuracao da janela
HEIGHT = 800
WIDTH = 400

# fps duh...
FPS = 60
# clock usado pra controlar o FPS
clock = pg.time.Clock()

# configuracoes das minas

# constantes que representam botoes do mouse
M_LCLICK = 1 # mouse left click
M_RCLICK = 3 # mouse right click

# configuracao da fonte
FONT_SIZE = 30
pg.font.init()
my_font = pg.font.SysFont("consolas", FONT_SIZE)
PERDEU_TEXT = my_font.render("Tu perdeu", False, [0, 0, 0])
GANHOU_TEXT = my_font.render("Tu ganhou", True, [0, 0, 0])


def game(WIDTH, HEIGHT, NUM_MINES):
    NUM_MINES = 3
    TOTAL_QUADRADOS = (WIDTH // 20) * (HEIGHT // 20)
    MAX_MINAS = TOTAL_QUADRADOS
    # funcao q resseta o jogo !!!FEIO PRA CARAMBA!!!
    def reset():
        nonlocal perdeu, won, first_click, mine_field, count_flags, count_revealed
        mine_field = MineField(WIDTH, HEIGHT, NUM_MINES)
        sprites.empty()
        sprites.add(mine_field.fields)
        count_flags = 0
        count_revealed = 0
        perdeu = False
        won = False
        first_click = True
    
    # n pode haver mais minas q quadrados
    if(NUM_MINES > MAX_MINAS):
        print("Tem minas demais!")
        sys.exit(-1)
    
    # init
    pg.init()
    pg.display.init()

    # configuracao da screen
    screen = pg.display.set_mode([WIDTH, HEIGHT + FONT_SIZE])
    screen.fill([255, 255, 255])
    pg.display.set_caption("Campo minado")
    pg.display.set_icon(pg.image.load(PATH + "/icons/icon.png"))

    # inicializacao do campo_minado
    mine_field = MineField(WIDTH, HEIGHT, NUM_MINES)

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
                # ressetar o jogo
                if(event.key == pg.K_F2):
                    reset()
                # mudar de tema
                if(event.key == pg.K_F9):
                    mine_field.toggle_theme()
            # quando clicka num quadrado (nao da pra clickar se o jogo tiver acabado)
            if(event.type == pg.MOUSEBUTTONDOWN and not perdeu and not won):
                # pega a posicao do mouse na hora do click
                x, y = event.pos

                # passa por todas as minas procurando a bomba dentro de x, y
                for mina in sprites:
                    # verifica se a coordenada [x, y] esta dentro do sprite atual
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

                            # o primeiro click temq ser em um espaco vazio
                            # TODO

                            # o botao esquerdo so funciona se estiver no estado default
                            if(mina.hiden == Field.DEFAULT):
                                # se vc clickar em uma bomba nao revelada (no estado default) vc perde
                                if(mina.number == Field.BOMB):
                                    perdeu = True
                                    # revela todas as bombas, ja q o jogo acabou
                                    mine_field.revelar()
                                    # seta a imagem da bomba explodida
                                    mina.set_bomb_exploded()  
                                # so da pra revelar as casas q estao sem bandeira/question
                                elif(mina.number == Field.EMPTY):
                                    # caso vc clicke em um quadrado vazio, o seu click "espalha" ate encontrar um numero
                                    mine_field.flood_fill(mina)
                                # clickou num numero
                                else:
                                    mina.on_left_click()

        # contar o numero de quadrados revelados
        count_revealed = 0    
        for mina in sprites:
            if(mina.hiden == Field.REVEALED):
                count_revealed += 1
        # so da pra ganhar se liberar todos os quadrados nao-bomba
        if(TOTAL_QUADRADOS - count_revealed == NUM_MINES):
            won = True

        # desenhando cada frame  

        screen.fill([100, 170, 255]) 

        # mostra a quantidade de minas q faltam (especulacao atravez das bandeiras)
        counter = NUM_MINES - count_flags
        text_count = my_font.render(str(counter), True, [200, 0, 0])
        text_rect = text_count.get_rect()
        text_rect.bottom = HEIGHT + FONT_SIZE + 2 # esse +2 eh pra centralizar... n sei pq o bottom n deu certo
        text_rect.right = WIDTH
        screen.blit(text_count, text_rect)


        # desenha as mensagens de vitoria/derrota na tela
        if(perdeu):
            # mostra PERDEU_TEXT na tela
            text_rect = PERDEU_TEXT.get_rect()
            text_rect.bottom = HEIGHT + FONT_SIZE
            text_rect.centerx = WIDTH // 2
            screen.blit(PERDEU_TEXT, text_rect)
        elif(won):
            screen.blit(GANHOU_TEXT, [WIDTH // 2 - PERDEU_TEXT.get_width() // 2, HEIGHT])
        
        # atualizacao da tela e dos sprites
        sprites.update()
        sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)