# Criado por Alexsander Rosante (12/03/20)

import pygame
import scripts.mouse
import scripts.objetos
from scripts import telas
from scripts import estado
from parametros.gerais import *
from parametros.cores import *
import sys


def main():

    pygame.init()

    tela = pygame.display.set_mode((tela_largura, tela_altura), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    loop = True

    # Inicializa os scripts
    mouse = scripts.mouse.Mouse()

    # Gerencia as telas
    estado.definir_tela(0, 'iniciar')

    # Inicializa as telas
    from scripts.estado import inventario_lista
    menuprincipal = telas.MenuPrincipal(tela)
    teladebatalha = telas.Batalha(tela, inventario_lista)
    mapa = telas.Mapa(tela, inventario_lista)

    while loop:

        clock.tick(fps)

        tela.fill(cinza_fundo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                loop = False

        mouse.update()
        entrada_teclado = pygame.key.get_pressed()

        # Gerenciamento de inventário
        from scripts.estado import remover_item
        if remover_item[0]:
            pass

        # Gerenciamento de telas no looping
        from scripts.estado import telacontexto, inventario_lista
        if telacontexto[0] == 0:  # Menu Principal
            menuprincipal.update(mouse.posicao, mouse.b_esquerdo, mouse.b_direito)
        elif telacontexto[0] == 1:
            if telacontexto[1] == 'iniciar':
                mapa = telas.Mapa(tela, inventario_lista)
                estado.definir_tela(1)
            mapa.update(mouse.posicao, mouse.b_esquerdo, mouse.b_direito, inventario_lista, entrada_teclado)
        elif telacontexto[0] == 2:  # Tela de batalha
            if telacontexto[1] == 'iniciar':
                teladebatalha = telas.Batalha(tela, inventario_lista)
                estado.definir_tela(2)
            teladebatalha.update(mouse.posicao, mouse.b_esquerdo, mouse.b_direito)

        estado.update()
        pygame.display.update()


main()
pygame.quit()
sys.exit()
