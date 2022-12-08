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
        self.background = pygame.transform.scale(LABaria_pict, (1200, 800))
        self.start_button = Button(350, 200, start_img_off, start_img_on, 1)
        self.load_save_button = Button(350, 400, load_save_off, load_save_on, 1)
        self.exit_button = Button(350, 600, exit_img_off, exit_img_on, 1)

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
            if self.world.will_collide_with_rect(0, -g, self.hero.rect):  # Проверяет можно ли еще чуть сместить героя
                self.hero.falling = False
            self.world.vy = 0
        else:
            self.hero.falling = True
        self.hero.set_animation(self.world.vx)
        self.world.move()

    def click_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
        self.screen.blit(self.background, (0, 0))
        self.start_button.draw_on(self.screen)
        self.exit_button.draw_on(self.screen)
        self.load_save_button.draw_on(self.screen)
        self.start_button.collide(self.screen)
        if self.exit_button.collide(self.screen):
            self.finished = True
        if self.load_save_button.collide(self.screen):
            print("In progress...")
        pygame.display.update()

    def run(self):
        while not self.finished:
            if not self.start_button.clicked:
                self.click_handler()
            else:
                self.clock.tick(60)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.finished = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        destroy_x, destroy_y = self.world.get_block(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                        self.world.break_block(destroy_x, destroy_y)
                self.world_move_general(pg.key.get_pressed())
                self.drawer.update_screen(self.world.map, self.hero, self.inventory)


if __name__ == "__main__":
    Game().run()
