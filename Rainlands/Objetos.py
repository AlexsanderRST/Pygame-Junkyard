# Criação de Alexsander Rosante

import pygame


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Imagens/Protagonista/imagem1.png')
        self.rect = self.image.get_rect(centerx=1366/2, bottom=499)

    def update(self):
        import Mouse



class Fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Imagens/Cenario/fundo.png')
        self.rect = self.image.get_rect()


class Camada1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([4098, 768], pygame.SRCALPHA)
        for i in range(3):
            imagem = pygame.image.load('Imagens/Cenario/chao.png')
            imagem_rect = imagem.get_rect(left=1366 * i)
            self.image.blit(imagem, imagem_rect)
        self.rect = self.image.get_rect()

    def update(self):
        teclado = pygame.key.get_pressed()
        if teclado[pygame.K_d]:
            self.rect.left -= 6
        elif teclado[pygame.K_a]:
            self.rect.left += 6
