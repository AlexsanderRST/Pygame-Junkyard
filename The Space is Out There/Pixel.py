# Criado por Alexsander Rosante

import pygame
from Sistema.parametros import *
from Sistema.cores import *


class Pixel(object):

    def __init__(self):

        # Superfície genérica
        self.superficie = pygame.Surface((1, 1))

        # Características
        self.lado, self.cor = tamanho_do_pixel, branco

        # Posição
        self.x, self.y = 0, 0
        self.altura_minima = fundo_altura - self.lado / 2 - 1

        # Fundamentais
        self.image = pygame.Surface((self.lado, self.lado))
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Estado
        self.gravidade = False

    def update(self):
        if self.gravidade:
            self.gravidade_()
        self.image.fill(self.cor)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
        self.superficie.blit(self.image, self.rect)

    def gravidade_(self):
        if self.y <= self.altura_minima:
            self.y += aceleracao_gravidade
