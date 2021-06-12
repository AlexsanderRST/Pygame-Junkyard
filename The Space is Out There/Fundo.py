# Criado por Alexsander Rosante

import pygame
from pygame.constants import *
from Bloco import Bloco
from Sistema.parametros import *


class Fundo(object):

    def __init__(self, superficie):

        # Superfície genérica
        self.superficie = superficie

        # Posição
        self.x, self.y = tela_centro
        self.xi, self.yi = self.x, self.y

        # Propriedades
        self.cor = cor_do_fundo
        self.quantidade_de_blocos = []
        self.lista_pixeis = []
        self.lista_blocos = []
        self.velocidade = 5

        # Fundamental
        self.image = pygame.Surface((fundo_largura, fundo_altura))
        self.image.fill(self.cor)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Montagem do fundo
        self.gerar_blocos(720)

    def update(self, entrada_teclado, posicao_mouse, mouse_besquerdo):
        posicao_mouse = self.relativizar_posicao_mouse(posicao_mouse)
        self.image.fill(self.cor)
        for i in self.lista_blocos: # For 1
            if len(i.lista) == 0:
                self.lista_blocos.remove(i)
            i.update(posicao_mouse, mouse_besquerdo)
        self.limite_pixeis()
        for i in self.lista_pixeis: # For 2
            i.update()
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)
        self.superficie.blit(self.image, self.rect)

    def gerar_blocos(self, quantidade_de_blocos):
        x, y = 0, fundo_altura // 2 + 80
        for i in range(quantidade_de_blocos):
            bloco = Bloco()
            bloco.superficie = self.image
            bloco.lista_superficie = self.lista_pixeis
            bloco.x, bloco.y = bloco.largura * x + bloco.centro[0], y + bloco.centro[1]
            x += 1
            if bloco.largura * x >= fundo_largura:
                x = 0
                y += bloco.altura
            self.lista_blocos.append(bloco)

    def limite_pixeis(self):
        if len(self.lista_pixeis) > limite_de_pixeis:
            self.lista_pixeis.pop(0)
            self.limite_pixeis()

    def relativizar_posicao_mouse(self, posicao_mouse):
        mouse_x = posicao_mouse[0] + (fundo_largura//2 - tela_centro[0]) + (self.xi - self.x)
        mouse_y = posicao_mouse[1] + (fundo_altura//2 - tela_centro[1]) + (self.yi - self.y)
        return mouse_x, mouse_y
