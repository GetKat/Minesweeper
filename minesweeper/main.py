import pygame as pg
import os
import sys

from field import Field
from minefield import MineField
from button import Button

# path para a pasta onde o programa esta rodando... n sei como funciona, pesquisar no stack overflow
PATH = os.path.dirname(os.path.abspath(__file__))

 # configuracao da janela
HEIGHT = 400
WIDTH = 400

# fps duh...
FPS = 60
# clock usado pra controlar o FPS
clock = pg.time.Clock()

# constantes que representam botoes do mouse
M_LCLICK = 1 # mouse left click
M_RCLICK = 3 # mouse right click

# cores
black = [0, 0, 0]
white = [255, 255, 255]
gray = [128, 128, 128]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
light_blue = [126, 126, 250]
orange = [250, 100, 0]
fire = [250, 160, 10] 

def game(WIDTH, HEIGHT, NUM_MINES):
    # configuracoes das minas
    TOTAL_QUADRADOS = (WIDTH // 20) * (HEIGHT // 20)
    MAX_MINAS = TOTAL_QUADRADOS

    # configuracao da fonte
    FONT_SIZE = 32
    pg.font.init()
    my_font = pg.font.SysFont("consolas", FONT_SIZE)
    PERDEU_TEXT = my_font.render("Tu perdeu", True, black, [100, 170, 255])
    GANHOU_TEXT = my_font.render("Tu ganhou", True, black, [100, 170, 255])

    # funcao q resseta o jogo !!!FEIO PRA CARAMBA!!!
    def reset():
        nonlocal perdeu, won, mine_field, count_flags, count_revealed
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
            # voltar ao menu principal
            if(event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                return
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
            text_rect.bottom = HEIGHT + FONT_SIZE + 2
            text_rect.centerx = WIDTH // 2
            screen.blit(PERDEU_TEXT, text_rect)
        elif(won):
            screen.blit(GANHOU_TEXT, [WIDTH // 2 - PERDEU_TEXT.get_width() // 2, HEIGHT])
        
        # atualizacao da tela e dos sprites
        sprites.update()
        sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

def main_menu():
    # configuracoes do jogo
    GAME_WIDTH = 300
    GAME_HEIGHT = 300
    GAME_NUM_MINES = 30

    # fonte
    pg.font.init()
    my_font = pg.font.SysFont("DaFont", 48)

    # init
    pg.display.init()
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])

    # sprites
    botoes = pg.sprite.Group()

    # config do texto
    text = my_font.render("Campo Minado", True, black, light_blue)
    text_rect = text.get_rect()
    text_rect.center = [WIDTH // 2, 50]

    # config da tela
    pg.display.set_caption("Menu Principal")

    # botoes
    names = ["Jogar", "Config", "Creditos", "Sair"]
    for i, name in enumerate(names):
        # origin - posicao vertical (eixo y) do primeiro botao
        origin = 100
        # dist - distancia entre um botao e outro
        dist = 50
        button_font = pg.font.SysFont("DaFont", 28)
        button = Button(WIDTH // 2, origin + dist * i, name, font = button_font, color = [orange, fire, black])
        botoes.add(button)

    on_menu = True
    while on_menu:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()

            # ver se clickou
            if(event.type == pg.MOUSEBUTTONUP):
                x, y = event.pos
                # ver em qual botao clickou
                for button in botoes:
                    if(button.rect.collidepoint([x, y])):
                        # ver oq fazer dependendo do botao clickado
                        if(button.text == "Sair"):
                            pg.quit()
                            sys.exit()
                        elif(button.text == "Jogar"):
                            # comeca o jogo
                            game(GAME_WIDTH, GAME_HEIGHT, GAME_NUM_MINES)
                            # dps q acaba o jogo, a janela volta ao tamanho inicial
                            screen = pg.display.set_mode([WIDTH, HEIGHT])
                        elif(button.text == "Config"):
                            backup = [GAME_WIDTH, GAME_HEIGHT, GAME_NUM_MINES]
                            opcoes(screen, backup)
                            GAME_WIDTH, GAME_HEIGHT, GAME_NUM_MINES = backup
                        elif(button.text == "Creditos"):
                            creditos(screen)

        # fundo da tela
        screen.fill(light_blue)

        # texto
        screen.blit(text, text_rect)

        # desenhando
        botoes.update()
        botoes.draw(screen)        

        # atualiza a tela
        pg.display.flip()

    # dps de ter saido do loop principal, limpa os sprites dos botoes
    botoes.empty()

def creditos(screen):
    # ajuste da tela
    screen.fill(black)

    # ajuste da fonte
    my_font = pg.font.SysFont("DaFont", 28)

    # cada nome em uma string, ler linha por linha do arquivo
    strings = []
    with open(PATH + "/credits.bin", "r") as file:
        string = file.readline()
        while string:
            # strip() remove os espaco em branco no inicio e final da string
            string = string.strip()
            strings.append(string)
            string = file.readline()

    # array de textos (surface object do pygame)
    texts = []
    for string in strings:
        text = my_font.render(string, True, white)
        texts.append(text)

    # loop da cena de creditos (sair ao apertar ESCAPE)
    on_credits = True
    while on_credits:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            # apertou a tecla escape
            if(event.type == pg.KEYUP):
                if(event.key == pg.K_ESCAPE):
                    on_credits = False

        screen.fill(black)
        # desenhar a palavra "Creditos" na tela
        creditos_msg = my_font.render("CREDITOS:", True, red, black)
        screen.blit(creditos_msg, [0, 0])

        # desenhar os creditos na tela
        y_distance = 32
        # y_distance - distancia entre cada linha (tamanho da fonte)
        for i, name in enumerate(texts):
            # name - text object
            start = 50
            # start - altura onde os nomes vao comecar a ser mostrados
            screen.blit(name, [0, start + i * 32])

        # desenhar "Aperte ESCAPE pra voltar" na tela
        escape_msg = pg.font.SysFont("DaFont", 20).render("PRESS ESCPAPE TO GO BACK", True, green, black)
        escape_msg_rect = escape_msg.get_rect()
        escape_msg_rect.right = WIDTH
        escape_msg_rect.bottom = HEIGHT
        screen.blit(escape_msg, escape_msg_rect)

        pg.display.flip()

# GAME_CONFIG = [GAME_WIDTH, GAME_HEIGHT, GAME_NUM_MINES]
def opcoes(screen, GAME_CONFIG):
    # ajuste da tela
    screen.fill(light_blue)

    # ajuste da fonte
    my_font = pg.font.SysFont("consolas", 42)

    # sprites
    buttons = pg.sprite.Group()

    # titulo
    titulo = my_font.render("Configuracoes:", True, black, light_blue)
    
    # mensagem "numero de bombas"
    bomb_font = pg.font.SysFont("consolas", 28)
    msg_bombas = bomb_font.render("numero de bombas:", True, black, light_blue)
    # mensagem "resolucao"
    msg_resolucao = bomb_font.render("resolucao: ", True, black, light_blue)

    # botoes de aumentar as bombas
    count_minas = Button(WIDTH // 2, 150, str(GAME_CONFIG[2]), font = my_font, color = [orange, fire, black], res = [70, 40], reactive = False)
    add = Button(WIDTH // 2 + 80, 150, "+", font = my_font, color = [orange, fire, black], res = [40, 40])
    sub = Button(WIDTH // 2 - 80, 150, "-", font = my_font, color = [orange, fire, black], res = [40, 40])

    # botao de aumentar a resolucao
    width_button = Button(WIDTH // 4, 250, str(GAME_CONFIG[0] // 20), font = my_font, color = [orange, fire, black], res = [100, 40], reactive = False)
    add_width = Button(WIDTH // 4 + 75, 250, "+", font = my_font, color = [orange, fire, black], res = [40, 40])
    add_width.id = "addw"
    sub_width = Button(WIDTH // 4 - 75, 250, "-", font = my_font, color = [orange, fire, black], res = [40, 40])
    sub_width.id = "subw"

    height_button = Button(3 * WIDTH // 4, 250, str(GAME_CONFIG[1] // 20), font = my_font, color = [orange, fire, black], res = [100, 40], reactive = False)
    add_height = Button(3 * WIDTH // 4 + 75, 250, "+", font = my_font, color = [orange, fire, black], res = [40, 40])
    add_height.id = "addh"
    sub_height = Button(3 * WIDTH // 4 - 75, 250, "-", font = my_font, color = [orange, fire, black], res = [40, 40])
    sub_height.id = "subh"

    # botao voltar ao menu
    voltar = Button(WIDTH // 2, HEIGHT - 50, "voltar", font = my_font, color = [orange, fire, black], res = [200, 40])

    buttons.add(count_minas, add, sub)
    buttons.add(width_button, add_width, sub_width)
    buttons.add(add_height, sub_height, height_button)
    buttons.add(voltar)

    on_config = True
    while on_config:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            
            # tecla escape sai do menu
            if(event.type == pg.KEYUP):
                if(event.key == pg.K_ESCAPE):
                    on_config = False

            if(event.type == pg.MOUSEBUTTONDOWN and event.button == M_LCLICK):
                x, y = event.pos
                for button in buttons:
                    if(button.rect.collidepoint([x, y])):
                        if(button.id == "addw"):
                            GAME_CONFIG[0] += 20
                        elif(button.id == "subw"):
                            GAME_CONFIG[0] -= 20
                        elif(button.id == "addh"):
                            GAME_CONFIG[1] += 20
                        elif(button.id == "subh"):
                            GAME_CONFIG[1] -= 20
                        elif(button.text == "+"):
                            GAME_CONFIG[2] += 1
                        elif(button.text == "-"):
                            GAME_CONFIG[2] -= 1
                        elif(button.text == "voltar"):
                            on_config = False

                        count_minas.text = str(GAME_CONFIG[2])
                        height_button.text = str(GAME_CONFIG[1] // 20)
                        width_button.text = str(GAME_CONFIG[0] // 20)


            # att
            screen.fill(light_blue)
            buttons.update()
            buttons.draw(screen)

            # titulo
            titulo_rect = titulo.get_rect()
            titulo_rect.centerx = WIDTH // 2
            screen.blit(titulo, titulo_rect)

            # msg das bombas
            bombas_rect = msg_bombas.get_rect()
            bombas_rect.centerx = WIDTH // 2
            bombas_rect.y = 100
            screen.blit(msg_bombas, bombas_rect)
            # msg da resolucao
            resolucao_rect = msg_resolucao.get_rect()
            resolucao_rect.centerx = WIDTH // 2
            resolucao_rect.y = 200
            screen.blit(msg_resolucao, resolucao_rect)

            pg.display.flip()


            ###button = Button(WIDTH // 2, origin + dist * i, name, font = button_font, color = [orange, fire, black])



def main():
    main_menu()

if(__name__ == "__main__"): main()
