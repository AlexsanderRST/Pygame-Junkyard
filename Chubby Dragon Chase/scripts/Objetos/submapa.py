# Criado por Alexsander Rosante (15/04/2020)

import pygame


class Submapa(pygame.sprite.Sprite):

    def __init__(self, cenario):
        pygame.sprite.Sprite.__init__(self)

        self.cenario = cenario
        # 0 -> Nunca Explorado; 1 -> Explorado; 2 -> Jogador sobre/ destacado;
        self.explorado = 0
        self.posicao = [0, 0]
        self.image = pygame.image.load('imagens/Submapas/' + cenario + '/base.png')
        if self.explorado == 0:
            mascara = pygame.image.load('imagens/Submapas/inexplorado.png')
            self.image.blit(mascara, mascara.get_rect())
        self.rect = self.image.get_rect()
        self.x, self.y, self.largura, self.altura = 0, 0, 100, 100
        self.interativo = False

    def update(self, posicao_jogador):  # Vai ter que mudar, muito pesado
        if posicao_jogador == self.posicao and self.explorado == 0:
            self.explorado = 1
            self.explorar()
        from scripts.estado import posicao_blocomestre
        self.rect = self.image.get_rect(centerx=self.x + posicao_blocomestre[0],
                                        centery=self.y + posicao_blocomestre[1])


    def explorar(self):
        self.image = pygame.image.load('imagens/Submapas/' + self.cenario + '/base.png')

    def adicionar_caminho(self, direcao):
        pass
