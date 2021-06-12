"""
A função desse script é gerenciar os objetos;
Criado por Alexsander Rosante
"""

from scripts.objetos import *
import random


class Principal(object):

    """
    Tela principal do jogo (Não confundir com menu principal)
    """

    def __init__(self, tela):
        self.tela = tela
        # partículas
        self.particulas_lado = pygame.sprite.Group()
        proxima_altura, espacamento = 0, 8
        for i in particulas_disponiveis:
            particula = Particula(i)
            particula.rect.topleft = (espacamento, proxima_altura + espacamento)
            particula.guardar_centro()
            proxima_altura = particula.rect.bottom
            self.particulas_lado.add(particula)
        self.particula_centro = pygame.sprite.GroupSingle()
        # colisores
        self.colisores = pygame.sprite.Group()
        self.colisor_centro = Colisor(visualizar=True)
        self.colisor_centro.rect.center = tela_largura / 2, tela_altura / 2
        self.colisor_superior = Colisor(visualizar=True)
        self.colisor_superior.rect.midtop = tela_largura/2, espacamento
        self.colisores.add(self.colisor_centro, self.colisor_superior)
        # estados
        self.ultima_cor = (0, 0, 0)
        self.particulas_misturadas = 0
        # cliente
        

    def update(self):
        self.colisores.update()
        # self.particulas_centro.update()
        self.particula_centro.update()
        self.particulas_lado.update()
        self.colisores.draw(self.tela)
        # self.particulas_centro.draw(self.tela)
        self.particula_centro.draw(self.tela)
        self.particulas_lado.draw(self.tela)

    def mouse_botao_esquerdo_pressionado(self, mouse_posicao):
        for particula in self.particulas_lado:
            if particula.rect.collidepoint(mouse_posicao):
                particula.selecionada = True
        for particula in self.particula_centro:
            if particula.rect.collidepoint(mouse_posicao):
                particula.selecionada = True

    def mouse_botao_esquerdo_solto(self):
        for particula_velha in self.particulas_lado:
            if particula_velha.rect.colliderect(self.colisor_centro.rect):
                self.particulas_misturadas += 1
                if self.particulas_misturadas <= 3:
                    if self.particulas_misturadas == 1:
                        particula_nova = Particula(misturar_cores(particula_velha.cor, False), 1)
                    else:
                        particula_nova = Particula(misturar_cores(particula_velha.cor, self.ultima_cor),
                                                   self.particulas_misturadas)
                    particula_nova.rect.center = tela_largura / 2, tela_altura / 2
                    particula_nova.guardar_centro()
                    self.particula_centro.add(particula_nova)
                    self.ultima_cor = particula_nova.cor
                    particula_velha.kill()
            elif particula_velha.rect.colliderect(self.colisor_superior):
                particula_velha.kill()
            particula_velha.desselecionar()

        for particula in self.particula_centro:
            if particula.rect.colliderect(self.colisor_superior):
                particula.kill()
            particula.desselecionar()


def misturar_cores(cor1, cor2):
    """
    :param cor1: cor da partícula selecionada pelo jogador
    :param cor2: cor da partícula que já está no centro
    :return: cor da nova partícula
    """
    cor = []
    if not cor2:
        cor = cor1
    elif cor1 == branco:
        for i in range(len(cor1)):
            if cor2[i] + 128 > 255:
                cor.append(255)
            else:
                cor.append(cor2[i] + 128)
    else:
        for i in range(len(cor1)):
            if cor1[i] + cor2[i] > 255:
                cor.append(255)
            else:
                cor.append(cor1[i] + cor2[i])
    return cor
