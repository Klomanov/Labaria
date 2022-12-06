import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *
from buttons import *


class Game:
    def __init__(self):
        pg.init()
        self.finished = False
        self.screen = pg.display.set_mode((width, height))
        self.drawer = visual.Drawer(self.screen)
        self.world = World(-1)
        spawn_block = self.world.get_block(hero_spawn_x, hero_spawn_y)
        self.hero = Hero(spawn_block.x, spawn_block.y)
        self.clock = pg.time.Clock()

    def world_move_general(self, keys):

        """Функция, которая осуществляет движение мира с помощью других функций в world.py"""

        if keys[pygame.K_a] and not self.world.will_collide_with_rect(hero_speed, 0, self.hero.rect):
            self.world.vx = hero_speed
        elif keys[pygame.K_d] and not self.world.will_collide_with_rect(-hero_speed, 0, self.hero.rect):
            self.world.vx = -hero_speed
        else:
            self.world.vx = 0

        if not self.world.will_collide_with_rect(0, self.world.vy-g, self.hero.rect):
            self.world.vy -= g
            self.hero.falling = True
        elif keys[pygame.K_SPACE]:
            self.world.vy = hero_jump_power
            self.hero.falling = True
        else:
            self.world.vy = 0
            self.hero.falling = False

        self.hero.set_animation(self.world.vx)
        self.world.move()

    def event_handler(self):
        """Функция-обработчик нажатий клавиш"""
        keys = pygame.key.get_pressed()
        self.world_move_general(keys)

    def run(self):
#        start_button = Button(350, 175, start_img_off, start_img_on, 1)
#        exit_button = Button(350, 375, exit_img_off, exit_img_on, 1)
        while not self.finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.finished = True
                self.clock.tick(60)
                self.event_handler()
                self.drawer.update_screen(self.world.map, self.hero)


if __name__ == "__main__":
    Game().run()
