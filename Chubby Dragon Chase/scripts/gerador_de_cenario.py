# Criado por Alexsander Rosante (25/03/2020)

# O usuário entra com um tipo de cenário (deserto, floresta)
# Retorna uma superfície

import pygame
from parametros.cores import *
from parametros.gerais import *
import random

cenario_largura, cenario_altura = 1440, 800
grade = 80

elementos_floresta = {1: 'grama',
                      2: 'flor',
                      3: 'pedra',
                      4: 'pedrinha',
                      5: 'flor2',
                      6: 'grama',
                      7: 'grama'}


def gerar_cenario(tipo, naodesenharem=()):
    if tipo == 'floresta':
        cenario = Cenario(verde_floresta)
        for i in range(cenario_altura // 80):
            for j in range(cenario_largura // 80):
                for k in range(1, 6):
                    if [j, i] not in naodesenharem:
                        n = random.randint(0, len(elementos_floresta))
                        if not n == 0:
                            elemento = pygame.image.load(
                                'imagens/gerador/' + tipo + '/' + elementos_floresta[n] + '_' + str(k) + '.png')
                            elemento_x = j * grade + grade // 2
                            elemento_y = i * grade
                            elemento_rect = elemento.get_rect(centerx=elemento_x, centery=elemento_y)
                            cenario.image.blit(elemento, elemento_rect)
        return cenario


class Cenario(pygame.sprite.Sprite):

    def __init__(self, cordosolo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((cenario_largura, cenario_altura))
        self.image.fill(cordosolo)
        self.rect = self.image.get_rect(centerx=tela_largura//2, centery=tela_altura//2)
