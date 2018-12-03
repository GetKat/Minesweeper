import pygame as pg, sys, os
import random
from field import Field

black = [0, 0, 0]
white = [255, 255, 255]
gray = [128, 128, 128]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

WIDTH = 400
HEIGHT = 400

N_MINAS = 10

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
    gerar_minas(fields)
    gerar_numeros(fields)
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

def gerar_minas(grid):
    count = 0
    while(count < N_MINAS):
        x, y = random.randint(0, WIDTH/20 - 1), random.randint(0, HEIGHT/20 - 1)
        if(grid[x][y].number != -1):
            grid[x][y].number = -1
            count += 1

# TODO otimizar a geracao de bomba (ir de bomba a bomba incrementando os quadrados adjacentes)
def gerar_numeros(grid):
    # verifica se a cordenada ta fora da matriz de campos
    def ok(i, j):
        return i >= 0 and j >= 0 and i < WIDTH / 20 and j < HEIGHT / 20
    # esse metodod passa quadrado por quadrado procurando uma bomba,
    # quando acha ele incrementa todos os valores dos quadrados adjacentes

    # direcao dos 8 quadrados adjacentes
    dir = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]

    for i in range(WIDTH//20):
        for j in range(HEIGHT//20):
            if(grid[i][j].number == -1): # achou a bomba
                for dir_i, dir_j in dir:
                    ii = i + dir_i
                    jj = j + dir_j
                    if(ok(ii, jj) and grid[ii][jj].number != -1): # se estiver na matriz e n for uma bomba (n incrementa o numero da bomba)
                        grid[ii][jj].number += 1

        
if(__name__ == '__main__'): main()