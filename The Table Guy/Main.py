# Criado por Alexsander Rosante

from pygame.constants import *
from Scripts.objetos import *
from Parametros.globais import *
from Parametros import imagens
from Parametros.cores import *
import sys


def main():

    pygame.init()

    tela = pygame.display.set_mode([tela_largura, tela_altura], FULLSCREEN, SCALED)

    loop = True

    relogio, fps = pygame.time.Clock(), 60

    grupo_estaticos = pygame.sprite.Group()

    principal = Estatico(imagens.principal, (684, 266))
    mesa = Estatico(imagens.mesa, (684, 428))

    grupo_estaticos.add(mesa, principal)
    grupo_estaticos.update()

    grupo_dinamicos = pygame.sprite.Group()

    smartfone = Dinamico(imagens.smartfone)
    smartfone.x, smartfone.y = 684, 330

    grupo_dinamicos.add(smartfone)

    while loop:

        relogio.tick(fps)

        tela.fill(branco)

        mouse_botao_esquerdo, mouse_meio, mouse_botao_direito = pygame.mouse.get_pressed()
        mouse_posicao = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == QUIT or evento.type == KEYDOWN and evento.key == K_ESCAPE:
                loop = False

        grupo_estaticos.draw(tela)

        grupo_dinamicos.update()
        grupo_dinamicos.draw(tela)

        pygame.display.update()


main()
pygame.quit()
sys.exit()
