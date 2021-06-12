# Criado por Alexsander Rosante

import pygame
from Sistema.parametros import *


class Jogador(object):

    def __init__(self, superficie):

        # Carrega as imagens do torso
        self.imagens_torso = [pygame.image.load("Imagens/Lindows/Torso/torso0.png")]

        # Carrega as imagens das rodas
        self.imagens_roda = []
        for i in range(9):
            imagem = pygame.image.load("Imagens/Lindows/Roda/roda" + str(i) + ".png")
            self.imagens_roda.append(imagem)

        # Frame
        self.frame_rodas = 0

        # Superfície genérica
        self.superficie = superficie

        # Características
        self.largura, self.altura = tamanho_do_pixel*pixeis_por_bloco, tamanho_do_pixel*pixeis_por_bloco*2
        self.image = pygame.image.load("Imagens/lindows.png")

        # Posição
        self.direcao = 1
        self.x, self.y = tela_centro[0], tela_centro[1]

    def update(self):

        # Atualizar rect
        rect = self.image.get_rect(centerx=self.x, centery=self.y)

        # Responsável pelas imagens do torso
        self.image = self.imagens_torso[0]
        if self.direcao < 0:
            self.image = pygame.transform.flip(self.image, True, False) # Essa conversão custa um pouco de processamento
        self.superficie.blit(self.image, rect)

        # Responsável pelas imagens das rodas
        self.image = self.animacao_rodas()
        if self.direcao < 0:
            self.image = pygame.transform.flip(self.image, True, False) # Essa conversão custa um pouco de processamento
        self.superficie.blit(self.image, rect)

    def animacao_rodas(self):
        if self.frame_rodas > 8:
            self.frame_rodas = 0
        return self.imagens_roda[self.frame_rodas]
