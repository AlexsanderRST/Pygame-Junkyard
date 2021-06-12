# Created by Alexsander Rosante

import pygame as pg
from numpy import linspace
from random import choice, randint

pg.init()

# configs
display_w = 1366
display_h = 768

# color
white = 255, 255, 255
gray = 128, 128, 128
black = 0, 0, 0


def main(bg_color=black):
    display = pg.display.set_mode([display_w, display_h], pg.FULLSCREEN)
    clock, fps = pg.time.Clock(), 60

    star = pg.sprite.Group()
    star2 = pg.sprite.Group()

    # configs
    n_star_max = 240
    n_star2_max = 480
    n_bg_stars = 500
    dur_min, dur_max = 240, 480
    dur_min2, dur_max2 = 480, 960
    jump = False

    while True:

        if not jump:
            display.fill(black)

        for ev in pg.event.get():
            if ev.type == pg.KEYUP:
                if ev.key == pg.K_ESCAPE:
                    return
                elif ev.key == pg.K_SPACE:
                    if jump:
                        jump = False
                    else:
                        jump = True

        if len(star) < n_star_max:
            star.add(Star(duration=randint(dur_min, dur_max)))
        if len(star2) < n_star2_max:
            star2.add(Star(white, 2, randint(dur_min2, dur_max2), 128))

        star.update()
        star2.update()
        star.draw(display)
        star2.draw(display)

        pg.draw.circle(display, black, (display_w // 2, display_h // 2), 100)

        clock.tick(fps)
        pg.display.update()


class Star(pg.sprite.Sprite):
    def __init__(self, color=white, radius_max=3, duration=60, alpha=255):
        pg.sprite.Sprite.__init__(self)

        # configs
        radius_min = 1
        self.dur = duration
        self.frame = 0
        self.clr = color
        self.alpha = alpha

        self.surf = pg.Surface(2 * [2 * radius_max], pg.SRCALPHA)
        self.image = self.surf.copy()
        self.rect = self.image.get_rect(center=(display_w // 2, display_h // 2))

        xf = randint(- display_w // 2, display_w + display_w // 2)
        if xf < 0 or xf > display_w:
            yf = randint(0, display_h)
        else:
            yf = choice((- radius_max // 2, display_h + radius_max // 2))
        self.move_x = linspace(display_w // 2, xf, duration)
        self.move_y = linspace(display_h // 2, yf, duration)
        self.grow = linspace(radius_min, radius_max, duration)

    def update(self):
        if self.frame < self.dur:
            self.image = self.surf.copy()
            circ_center = self.image.get_size()[0] // 2, self.image.get_size()[1] // 2
            pg.draw.circle(self.image, self.clr, circ_center, int(self.grow[self.frame]))
            self.rect.center = self.move_x[self.frame], self.move_y[self.frame]
            self.image.set_alpha(self.alpha)
            self.frame += 1
        else:
            self.kill()


main()
pg.quit()
