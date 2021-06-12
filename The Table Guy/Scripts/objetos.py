# Criado por Alexsander Rosante

import pygame


class Estatico(pygame.sprite.Sprite):

    def __init__(self, imagem, pos):

        pygame.sprite.Sprite.__init__(self)

        self.x, self.y = pos[0], pos[1]

        self.image = pygame.image.load(imagem)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)


class Dinamico(pygame.sprite.Sprite):

    def __init__(self, imagem):

        pygame.sprite.Sprite.__init__(self)

        self.x, self.y = 0, 0

        self.image = pygame.image.load(imagem)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

    def update(self):

        self.interacao()

        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

    def interacao(self):
        pass
