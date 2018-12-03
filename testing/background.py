import pygame, sys

WIDTH = 600
HEIGHT = 600

white = [255, 255 ,255]
black = [0, 0, 0]
red = [255, 0 ,0]
blue = [0, 0, 255]

def main():
    # muda o background se apertar 0, 9 e 2
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Eae meu brother")
    screen.fill(white)

    text = pygame.font.SysFont('Times new roman', 40).render("Eeae K K K K K ", True, [10, 10, 20, 20])

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    screen.fill(black)
                if event.key == pygame.K_9:
                    screen.fill(blue)
                if event.key == pygame.K_2:
                    screen.blit(text, [10, 10, 20, 20])
            if event.type == pygame.KEYUP:
                screen.fill(white)
            
                
main()