# Criado por Alexsander Rosante

from pygame.locals import *
from scripts.ambiente import *


def main():

    pygame.init()

    tela = pygame.display.set_mode([tela_largura, tela_altura], FULLSCREEN)

    ambiente = Principal(tela)

    while True:

        tela.fill((0, 0, 0))

        for evento in pygame.event.get():
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    return False
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    ambiente.mouse_botao_esquerdo_pressionado(evento.pos)
            elif evento.type == MOUSEBUTTONUP:
                if evento.button == 1:
                    ambiente.mouse_botao_esquerdo_solto()

        ambiente.update()

        pygame.display.update()

main()
