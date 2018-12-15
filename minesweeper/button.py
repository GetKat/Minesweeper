import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, x = 0, y = 0, text = "Undefined", reactive = True, font = None, res = [140, 40], color = [[255, 0, 0], [0, 255, 0], [255, 255, 255]]):
        # color [background, when touched, text color]
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(res)
        self.image.fill(color[0])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # estilo da fonte
        self.font = font
        # texto q vai aparecer no botao
        self.text = text
        # ver se ele reage ao mouse ou n
        self.reactive = reactive
        # cor do botao
        self.color = color

        self.id = ""

    def update(self):
        x, y = pg.mouse.get_pos()
        sprite_rect = self.rect

        self.image.fill(self.color[0])
        text = self.font.render(self.text, True, self.color[2], self.color[0])

        # cores do botao
        if(self.reactive):
            mouse_over = sprite_rect.collidepoint([x, y])
            if(mouse_over):
                self.image.fill(self.color[1])
                text = self.font.render(self.text, True, self.color[2], self.color[1])
        # botar o texto
            # pegar o texto
        
        text_rect = text.get_rect()

            # desenhando o texto no meio do sprite, por isso eu preciso da coordenada da imagem (ao invez da tela completa)
        text_rect.center = self.image.get_rect().center

        self.image.blit(text, text_rect)
