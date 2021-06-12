# Criado por Alexsander Rosante

import pygame
from scripts.parametros import *
import numpy as np


class Particula(pygame.sprite.Sprite):

    """Objeto principal do jogo.
    Ela inicia no canto da tela e o jogador pode arrastá-la com o mouse"""

    def __init__(self, cor, tamanho=1):
        pygame.sprite.Sprite.__init__(self)
        self.cor, self.tamanho = cor, tamanho  # posteriormente usarei o self.tamanho
        self.raio = particula_raio * self.tamanho
        self.selecionada = False
        self.image = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        # desenha a particula
        pygame.draw.circle(self.image, self.cor,
                           (round(self.image.get_size()[0] / 2), round(self.image.get_size()[1] / 2)), self.raio)
        # armazena alguns dados
        self.centroi = self.rect.center
        self.animacao = self.AnimacaoParada()
        # olhos

    def update(self):
        if self.selecionada:
            self.rect = self.image.get_rect(center=pygame.mouse.get_pos())
        self.animacao.update(self)

    def desselecionar(self):
        if self.selecionada:
            self.animacao = self.AnimacaoVoltarMenu(particula=self)
            self.selecionada = False

    def guardar_centro(self):
        self.centroi = self.rect.center

    class AnimacaoParada(object):
        def __init__(self):
            pass

        def update(self, *args):
            pass

    class AnimacaoVoltarMenu(object):
        def __init__(self, particula):
            tempo = 120  # frames
            xi, xf = particula.centroi[0], particula.rect.centerx
            yi, yf = particula.centroi[1], particula.rect.centery
            self.array_x = np.linspace(xf, xi, tempo)
            self.array_y = np.linspace(yf, yi, tempo)
            self.frame = 0

        def update(self, particula):
            particula.rect.center = (self.array_x[self.frame], self.array_y[self.frame])
            if self.frame == len(self.array_x) - 1:
                particula.animacao = particula.AnimacaoParada()
            self.frame += 1

    class AnimacaoCair(object):
        def __init__(self, particula):
            self.tempo = 120  # frames
            self.yi, yf = particula.centroi[1], tela_altura + particula.image.get_size()[1] / 2
            self.aceleracao = (2 * (yf - self.yi)) / self.tempo ** 2
            self.frame = 0

        def update(self, particula):
            particula.rect.centery = self.yi + (self.aceleracao / 2) * self.frame ** 2
            if self.frame >= self.tempo:
                particula.animacao = particula.AnimacaoParada()
            self.frame += 1


class Colisor(pygame.sprite.Sprite):
    """Detecta uma colisão entre rects e retorna uma função"""
    def __init__(self, largura=particula_raio * 6, altura=particula_raio * 6, visualizar=False):
        pygame.sprite.Sprite.__init__(self)
        self.largura, self.altura = largura, altura
        self.cor_normal, self.cor_alvejado = (128, 128, 128), (255, 255, 0)
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.visivel = visualizar

    def update(self, *args):
        if self.visivel:
            self.image = pygame.Surface((self.largura, self.altura))
            if not self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image.fill(self.cor_normal)
            else:
                self.image.fill(self.cor_alvejado)
        else:
            self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
