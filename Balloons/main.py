"""
Created by Alexsander Rosante
"""

import pygame, sys, os
from pygame.locals import *
from random import randint

version = '1.0'
fps = 60

# colors
lightskyblue = 135, 206, 250

# configs
uplift_speed = 4
wind_speed = 0
balloons_layers = 3

# mouse pos
mouse_pos = 0, 0


def main():
    global wind_speed, mouse_pos
    pygame.init()
    flags = HWSURFACE
    display = pygame.display.set_mode((800, 600), flags)
    pygame.display.set_caption('Ballons ' + version)
    pygame.display.set_icon(pygame.image.load('imgs/icon.png'))
    clock = pygame.time.Clock()

    balloons = Balloons(display)

    while True:

        display.fill(lightskyblue)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_d:
                    wind_speed += 1
                elif event.key == K_a:
                    wind_speed -= 1
            elif event.type == QUIT:
                pygame.quit()
                return

        balloons.update()
        balloons.draw(display)

        clock.tick(fps)
        pygame.display.flip()


class Balloons(pygame.sprite.LayeredUpdates):

    def __init__(self, display):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.display = display
        self.timming = 0
        self.kill_method = 1

    def update(self, max_balloons=50):
        pygame.sprite.LayeredUpdates.update(self)
        self.refill()
        self.set_kill_method()

    def set_kill_method(self):
        if -10 < wind_speed < 10 and self.kill_method != 1:
            self.kill_method = 1
            for baloon in self:
                baloon.kill_method = baloon.kill_method_1
        elif wind_speed < -10 and self.kill_method != 2:
            self.kill_method = 2
            for baloon in self:
                baloon.kill_method = baloon.kill_method_2
        elif wind_speed > 10 and self.kill_method != 3:
            self.kill_method = 3
            for baloon in self:
                baloon.kill_method = baloon.kill_method_3

    def refill(self, max_ballons=50):
        if len(self) <= max_ballons:
            if self.timming == 10:
                ballon_layer = randint(1, balloons_layers)
                ballon = Balloon(self.display, ballon_layer)
                self.add(ballon)
                self.change_layer(ballon, balloons_layers - ballon_layer)
                self.timming = 0
            else:
                self.timming += 1


class Balloon(pygame.sprite.Sprite):

    def __init__(self, display, layer=1):
        pygame.sprite.Sprite.__init__(self)
        self.display_width = display.get_width()
        self.display_height = display.get_height()
        self.image = pygame.image.load('imgs/balloon{0}_{1}.png'.format(str(randint(1, 4)),
                                                                        layer))
        if -10 < wind_speed < 10:
            self.rect = self.image.get_rect(centerx=randint(0, self.display_width),
                                            top=self.display_height)
        elif wind_speed < -10:
            self.rect = self.image.get_rect(left=self.display_width,
                                            centery=randint(0, self.display_height))
        else:
            self.rect = self.image.get_rect(right=0,
                                            centery=randint(0, self.display_height))

        if layer == 1:
            self.image.set_alpha(230)
            self.move = self.move_layer1
        elif layer == 2:
            self.image.set_alpha(191)
            self.move = self.move_layer2
        else:
            self.image.set_alpha(128)
            self.move = self.move_layer3

        self.kill_method = self.kill_method_1

    def update(self):
        self.kill_method()

    def move_layer1(self):
        self.rect.centerx += wind_speed
        self.rect.centery -= uplift_speed

    def move_layer2(self):
        self.rect.centerx += wind_speed / 2
        self.rect.centery -= uplift_speed / 2

    def move_layer3(self):
        self.rect.centerx += wind_speed / 4
        self.rect.centery -= uplift_speed / 4

    def kill_method_1(self):
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.move()

    def kill_method_2(self):
        if self.rect.right <= 0:
            self.kill()
        else:
            self.move()

    def kill_method_3(self):
        if self.rect.left >= self.display_width:
            self.kill()
        else:
            self.move()


if __name__ == '__main__':
    main()
