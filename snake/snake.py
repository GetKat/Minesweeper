import pygame as pg, sys, random

black = [0, 0, 0]
white = [255, 255, 255]
gray = [128, 128, 128]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

HEIGHT = 300
WIDTH = 300

sprites = pg.sprite.Group()
clock = pg.time.Clock()

def main():
    # init's
    pg.init()
    pg.display.init()
    pg.display.set_caption("Cobrinha")
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    screen.fill(black)
    # sprite
    snake = Snake()
    food = Food()
    sprites.add(food)
    sprites.add(snake.sprite_buffer)


    while True:
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                sys.exit()
            if(event.type == pg.KEYDOWN):
                arrows = {
                    pg.K_UP: [0, -1],
                    pg.K_DOWN: [0, 1],
                    pg.K_LEFT: [-1, 0],
                    pg.K_RIGHT: [1, 0]
                }
                snake.update(arrows.get(event.key, None))
                if(event.key == pg.K_SPACE):
                    snake.grow()

        snake.move()
        sprites.update()

        if(snake.get_head_rect() == food.get_rect()):
            snake.grow()
            food.update_pos()

        sprites.update()

        screen.fill(black)
        sprites.draw(screen)
        pg.display.flip()
        clock.tick(15)

        if(snake.dead()):
            print("Vc morreu!")
            pg.quit()
            input()
            return

class Food(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([10, 10])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH/10 - 1) * 10
        self.rect.y = random.randint(0, HEIGHT/10 - 1) * 10

    def update_pos(self):
        self.rect.x = random.randint(0, WIDTH/10 - 1) * 10
        self.rect.y = random.randint(0, HEIGHT/10 - 1) * 10

    def get_rect(self):
        return self.rect.copy()

class Body(pg.sprite.Sprite):
    def __init__(self, head = False, x = WIDTH / 2, y = HEIGHT / 2):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([10, 10])
        self.image.fill(red if head else blue)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.head = head

class Snake:
    def __init__(self):
        self.sprite_buffer = [Body(True, 100, 90)]
        self.direction = [1, 0]

        self.n_grow = 0

    def move(self):
        # movo a cabeca e dps cada parte segue a da frente
        for body in self.sprite_buffer:
            if(body.head):
                cur_rect = body.rect.copy()
                body.rect.x += self.direction[0] * 10
                body.rect.y += self.direction[1] * 10
            else:
                cur_rect, body.rect = body.rect, cur_rect

            if(self.n_grow > 0):
                new = Body(False, cur_rect.x, cur_rect.y) 
                self.sprite_buffer.append(new)
                sprites.add(new)
                self.n_grow -= 1

            # n sair da tela
            if(body.rect.top < 0):
                body.rect.bottom = HEIGHT
            if(body.rect.bottom > HEIGHT):
                body.rect.top = 0
            if(body.rect.left < 0):
                body.rect.right = WIDTH
            if(body.rect.right > WIDTH):
                body.rect.left = 0
    
    def update(self, direction):
        if(direction != None):
            if(direction[0] != self.direction[0] and direction[1] != self.direction[1]):
                self.direction = direction

    def grow(self, n_value = 1):
        self.n_grow = n_value

    def dead(self):
        # verifico se tem dois Body's na mesma posicao
        for body in self.sprite_buffer:
            rect = body.rect
            for other_body in self.sprite_buffer:
                if(body != other_body and rect == other_body.rect):
                    return True
        return False
    
    def get_head_rect(self):
        return self.sprite_buffer[0].rect.copy()



if __name__ == '__main__': main()