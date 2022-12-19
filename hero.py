import pygame as pg
from constants import *
import visual


class Hero(visual.DrawableObject):
    def __init__(self, x, y):
        self.animCount = 0
        self.x = x
        self.y = y
        self.falling = False
        self.animation = Animations.static[0]
        self.image = pg.transform.scale(self.animation, (hero_width, hero_height))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.breaking_block = None
        self.breaking_start_time = None
        self.selected_item_type = None

    def set_animation(self, vx):
        if self.breaking_block is not None:
            self.animation = Animations.break_down
        else:
            if self.falling and vx > 0:
                self.animation = Animations.jump_left
            elif self.falling and vx < 0:
                self.animation = Animations.jump_right
            elif vx > 0:
                self.animation = Animations.left
            elif vx < 0:
                self.animation = Animations.right
            else:
                self.animation = Animations.static

    def draw_on(self, screen):
        if self.animCount + 1 >= 35:
            self.animCount = 0

        if self.animation == Animations.static or self.animation == Animations.jump_left or self.animation == Animations.jump_right:
            self.image = self.animation[0]
        else:
            self.image = self.animation[self.animCount // 5]
            self.animCount += 1

        screen.blit(self.image, self.rect)


def hero_main():
    """Рисует героя в пустоте."""
    screen = pg.display.set_mode((1200, 800))
    pg.display.set_caption('Hero')
    hero = Hero(screen_width/2, screen_height/2)
    run = True
    vx = 0
    while run:
        screen.fill((100, 249, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                vx = hero_speed
            if keys[pg.K_d]:
                vx = -hero_speed
            if not keys[pg.K_a] and not keys[pg.K_d]:
                vx = 0
            if keys[pg.K_SPACE]:
                hero.falling = True
            if keys[pg.K_s]:
                hero.falling = False
        hero.set_animation(vx)
        hero.draw_on(screen)
        pg.display.update()


if __name__ == "__main__":
    hero_main()
