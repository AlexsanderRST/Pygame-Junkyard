# Criação de Alexsander Rosante

from Tela import *
import Mouse

pygame.init()


def main():

    tela = pygame.display.set_mode([1366, 768], pygame.FULLSCREEN)
    clock, fps = pygame.time.Clock(), 60
    loop = True

    ambiente = Cenario1(tela)


    while loop:

        clock.tick(fps)
        Mouse.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = False

        ambiente.update()
        pygame.display.update()

main()
pygame.quit()
