import pygame
import math
from random import randint


class Sky(pygame.sprite.Group):
    def __init__(self, display_w, display_h, n_stars=1000, bg_color=(0, 0, 0)):
        pygame.sprite.Group.__init__(self)
        self.bg_color = bg_color
        for i in range(n_stars):
            star = Star()
            star.rect.center = randint(0, display_w), randint(0, display_h)
            self.add(star)

    def update(self, display):
        display.fill(self.bg_color)
        pygame.sprite.Group.update(self)


class Star(pygame.sprite.Sprite):
    def __init__(self, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.frame = randint(0, 10)

    def update(self):
        self.image.set_alpha(int(math.sin(self.frame * 1 / 2) * 127 + 127))
        self.frame += 0.07
