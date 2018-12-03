import pygame as pg, sys

white = [255, 255 ,255]
red = [255, 0 ,0]
blue = [0, 0, 255]

def main():
    # display text when key 2 is pressed
    pg.init()
    pg.display.init()
    pg.font.init()

    screen = pg.display.set_mode([600, 600])
    screen.fill(white)
    pg.display.set_caption("Eae")

    my_font = pg.font.SysFont('Arial', 30)
    text = my_font.render("Hello", True, blue)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_2:
                    screen.blit(text, [0, 0])
        pg.display.update()

    print(screen.get_rect())

main()