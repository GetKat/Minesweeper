import pygame, sys

white = [255, 255 ,255]
red = [255, 0 ,0]
blue = [0, 0, 255]

def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode([400, 400])
    pygame.display.set_caption("Hello world")

    screen.fill(white)

    count = 0
    cur = 0,0
    pygame.draw.rect(screen, red, [10, 10, 20, 20])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos[0], event.pos[1])
                count += 1
                if(count == 2):
                    count = 0
                    pygame.draw.line(screen, blue, cur, event.pos)
                pygame.draw.line(screen, blue, event.pos, event.pos)
                cur = event.pos

        pygame.display.update()

main()
