# Criado por Alexsander Rosante (12/03/20)

import pygame


class Mouse(object):

    def __init__(self):

        self.posicao = (0, 0)
        self.b_esquerdo, self.b_meio, self.b_direito = False, False, False
        self.b_pressionado = [False, None]  # [Está pressionado?, Qual?]
        self.b_esquerdo_anterior, self.b_direito_anterior = False, False

    def update(self):

        # Coleta informações de entrada
        self.posicao = pygame.mouse.get_pos()
        self.b_esquerdo, self.b_meio, self.b_direito = pygame.mouse.get_pressed(3)

        # Corrige cliques fantasmas com o botão esquerdo
        if self.b_esquerdo:
            if not self.b_esquerdo_anterior:
                self.b_esquerdo_anterior = True
            else:
                self.b_esquerdo = False
        else:
            if self.b_esquerdo_anterior:
                self.b_esquerdo_anterior = False
