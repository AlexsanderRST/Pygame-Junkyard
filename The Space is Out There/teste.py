import pygame
from pygame.constants import *
import sys

tela_largura, tela_altura = 1366, 768
tela_meio = (tela_largura//2, tela_altura//2)
tela = pygame.display.set_mode((1366, 768), FULLSCREEN)

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

pygame.init()

# Essenciais
loop = True
clock, fps = pygame.time.Clock(), 60


class Bloco(pygame.sprite.Sprite):

    def __init__(self, superficie):
        pygame.sprite.Sprite.__init__(self)
        self.superficie = superficie
        self.largura, self.altura, self.cor = 100, 100, branco
        self.x, self.y = 0, 0
        self.image = pygame.Surface((self.largura, self.altura))
        self.image.fill(branco)
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill(self.cor)
        self.rect = self.image.get_rect(centerx=self.x, centery=self.y)

blocoA = Bloco(tela)
blocoB = Bloco(tela)
blocoB.x, blocoB.y = tela_meio[0], tela_meio[1]

lista_de_sprites = pygame.sprite.Group()
lista_de_sprites2 = pygame.sprite.Group()
lista_de_sprites.add(blocoA)
lista_de_sprites2.add(blocoB)

while loop:

    clock.tick(fps)

    tela.fill(preto)

    mouse_e, mouse_m, mouse_d = pygame.mouse.get_pressed()
    posicao_mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            loop = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = False
            elif event.key == K_SPACE:
                blocoA.cor = vermelho

    if mouse_e and not pygame.sprite.spritecollide(blocoA, lista_de_sprites2, False):
        if blocoA.rect.collidepoint(posicao_mouse):
            blocoA.x, blocoA.y = posicao_mouse
    elif not mouse_e and pygame.sprite.spritecollide(blocoA, lista_de_sprites2, False):
        blocoA.x -= 1

    lista_de_sprites.update()
    lista_de_sprites2.update()
    lista_de_sprites.draw(tela)
    lista_de_sprites2.draw(tela)

    pygame.display.update()

pygame.quit()
sys.exit()