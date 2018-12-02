import random

WIDTH = 400
HEIGHT = 400


m = [[0 for i in range(0, WIDTH, 20)] for j in range(0, HEIGHT, 20)]

def main():
    MINAS = 1
    count_minas = 0
    minas = []

    while(count_minas < MINAS):
        x, y = random.randint(0, 19), random.randint(0, 19)
        if(m[x][y] == 0):
            m[x][y] = -1
            count_minas += 1
            minas.append([x, y])

    for mina in minas:
        calcular_numeros(mina)
    print_m(m)

def calcular_numeros(coord):
    i = coord[0]
    j = coord[1]
    dir_i = [-1, -1, -1, 0, 1, 1, 1, 0]
    dir_j = [-1, 0, 1, 1, -1, 0, -1, -1]
    for k in range(len(dir_i)):
        ii = i + dir_i[k]
        jj = j + dir_j[k]
        if(ok(ii, jj)):
            print(ii, jj)
            m[ii][jj] += 1
        


def ok(i, j):
    return i >= 0 and j >= 0 and i < WIDTH / 20 and j < HEIGHT / 20

def print_m(m):
    for rows in m:
        print(rows)


if(__name__ == '__main__'): main()