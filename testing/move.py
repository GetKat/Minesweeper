import pygame as pg, sys

white = [255, 255 ,255]
black = [0, 0, 0]
red = [255, 0 ,0]
blue = [0, 0, 255]
gray = [126, 126, 126]

steps = 10

clock = pg.time.Clock()

def main():
    # move a box arround the screen using arrow keys
    state = {
        pg.K_DOWN: [0, 1],
        pg.K_UP: [0, -1],
        pg.K_RIGHT: [1, 0],
        pg.K_LEFT: [-1, 0]
    }
    box = Box()
    pg.init()
    pg.display.init()

    screen = pg.display.set_mode([600, 600])
    screen.fill(gray)

    direct = state[pg.K_RIGHT]
    while True:
        pg.display.update()
        pg.draw.rect(screen, red, box.get_pos() + [10, 10])
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                direct = state.get(event.key, direct)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        box.update(steps * direct[0], steps * direct[1])
        print('postion: ', box.get_pos())
        if box.x < 0:
            box.x = 600
        elif box.x >= 600:
            box.x = 0
        elif box.y < 0:
            box.y = 600
        elif box.y >= 600:
            box.y = 0
        pg.draw.rect(screen, blue, box.get_pos() + [10, 10])
        clock.tick(50)    

class Box:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self):
        return [self.x, self.y]

main()