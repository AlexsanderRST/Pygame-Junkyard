import pygame
from sky import Sky


def main(fps=60):
    pygame.init()
    display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    display_w, display_h = pygame.display.Info().current_w, pygame.display.Info().current_h
    clock = pygame.time.Clock()

    sky = Sky(display_w, display_h)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        sky.update(display)
        sky.draw(display)

        clock.tick(fps)
        pygame.display.update()


main()
