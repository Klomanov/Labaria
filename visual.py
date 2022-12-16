import pygame as pg
from constants import *


def is_chunk_on_screen(chunk):
    for block in chunk[0]:
        if screen_width + 2 * block_size >= block.x >= -2 * block_size:
            return True
    return False


def is_block_on_screen(block):
    return screen_width + 2 * block_size >= block.x >= -2 * block_size and\
           screen_height + 2 * block_size >= block.y >= -2 * block_size


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update_screen(self, map, hero, inventory):
        """
        Рисует все объекты на экране и обновляет его
        :param inventory:
        :param world:
        :param hero:
        :return:
        """
        self.screen.fill((0, 0, 0))
        for chunk in map:
            if is_chunk_on_screen(chunk):
                for row in chunk:
                    for block in row:
                        if is_block_on_screen(block):
                            block.draw_on(self.screen)
        hero.draw_on(self.screen)
        inventory.draw_on(self.screen)
        pg.display.update()


class DrawableObject:
    def draw_on(self, surface):
        pass
