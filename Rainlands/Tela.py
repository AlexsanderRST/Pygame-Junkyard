# Criação de Alexsander Rosante

from Objetos import *


class Cenario1(object):
    def __init__(self, tela):
        self.tela = tela
        self.grupo = pygame.sprite.Group(Fundo(), Camada1(), Jogador())

    def update(self):
        self.grupo.update()
        self.grupo.draw(self.tela)
