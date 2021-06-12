# Criação de Alexsander Rosante

import pygame

posicao = [0, 0]
LMB = 0
espera = 0


def update():
    global posicao, LMB, espera
    posicao = pygame.mouse.get_pressed()
    LMB = pygame.key.get_pressed()[0]
    if espera > 0:
        if LMB:
            LMB = 0
        espera -= 1
    else:
        if LMB:
            espera = 6
