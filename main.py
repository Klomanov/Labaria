import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *
from buttons import *
from inventory import *


class Game:
    def __init__(self):
        pg.init()
        self.finished = False
        self.screen = pg.display.set_mode((width, height))
        self.drawer = visual.Drawer(self.screen)
        self.world = World(-1)
        spawn_block_x, spawn_block_y = self.world.get_block(hero_spawn_x, hero_spawn_y)
        spawn_block = self.world.map[spawn_block_y][spawn_block_x]
        self.hero = Hero(spawn_block.x, spawn_block.y)
        self.clock = pg.time.Clock()
        self.inventory = Inventory(self.screen)

    def world_move_general(self, keys):

        """Функция, которая осуществляет движение мира с помощью других функций в world.py"""

        if keys[pygame.K_a]:
            self.world.vx = hero_speed
        if keys[pygame.K_d]:
            self.world.vx = -hero_speed

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.world.vx = 0

        self.world.vy -= g
        if keys[pygame.K_SPACE] and not self.hero.falling:
            self.world.vy += hero_jump_power

        if self.world.will_collide_with_rect(self.world.vx, 0, self.hero.rect):
            self.world.vx = 0
        if self.world.will_collide_with_rect(0, self.world.vy, self.hero.rect):
            if self.world.vy < 0:
                self.hero.falling = False
            self.world.vy = 0
        else:
            self.hero.falling = True
        self.hero.set_animation(self.world.vx)
        self.world.move()

    def run(self):
        # start_button = Button(400, 300, start_img, 0.5)
        while not self.finished:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.finished = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    destroy_x, destroy_y = self.world.get_block(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    self.world.brake_block(destroy_x, destroy_y)
            self.world_move_general(pg.key.get_pressed())
            self.drawer.update_screen(self.world.map, self.hero)


if __name__ == "__main__":
    Game().run()
