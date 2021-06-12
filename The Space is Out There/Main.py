# Criado por Alexsander Rosante

import pygame
from Fundo import Fundo
from Entidades import Jogador
from Sistema.parametros import *
from Sistema.cores import *
from pygame.constants import *
import sys

pygame.init()

Tela = pygame.display.set_mode((tela_largura, tela_altura), FULLSCREEN)

# Fundamentais
Loop = True
Clock, FPS = pygame.time.Clock(), 60
lista_Tela = []

# Fundo
fundo = Fundo(Tela)

# Protagonista
jogador = Jogador(Tela)

while Loop:

    # Limitador de quadros
    Clock.tick(FPS)

    # Cor da tela
    Tela.fill(branco)

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            Loop = False

    # Checa as entradas, mouse e teclado, disponibilizando variáveis booleanas
    mouse_besquerdo, mouse_bmeio, mouse_bdireito = pygame.mouse.get_pressed()
    posicao_mouse = pygame.mouse.get_pos()
    entrada_teclado = pygame.key.get_pressed()

    # Comandos
    if entrada_teclado[K_d]:
        jogador.frame_rodas += 1
        jogador.direcao = 1
        fundo.x -= fundo.velocidade
    elif entrada_teclado[K_a]:
        jogador.frame_rodas += 1
        jogador.direcao = -1
        fundo.x += fundo.velocidade

    fundo.update(entrada_teclado, posicao_mouse, mouse_besquerdo)

    # Parte do loop voltada ao protagonista
    jogador.update()

    pygame.display.update()

pygame.quit()
sys.exit()
