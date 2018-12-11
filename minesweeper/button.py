import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, x = 0, y = 0, text = "Undefined"):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([100, 40])
        self.image.fill([255, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # texto q vai aparecer no botao
        self.text = text

    def update(self):
        x, y = pg.mouse.get_pos()
        sprite_rect = self.rect

        # cores do botao
        mouse_over = sprite_rect.collidepoint([x, y])
        if(mouse_over):
            self.image.fill([0, 255, 0])
        else:
            self.image.fill([255, 0, 0])

        # botar o texto
            # fonte
        font = pg.font.SysFont("DaFont", 24)
            # pegar o texto
        text = font.render(self.text, True, [255, 255, 255])
        text_rect = text.get_rect()

            # desenhando o texto no meio do sprite, por isso eu preciso da coordenada da imagem (ao invez da tela completa)
        text_rect.center = self.image.get_rect().center

        self.image.blit(text, text_rect)
