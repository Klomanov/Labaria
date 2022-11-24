import pygame as pg


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def display_world(self, world):
        self.screen.fill((0, 0, 0))
        for row in world:
            for block in row:
                block.draw_on(self.screen)
        pg.display.update()


class DrawableObject:
    def draw_on(self, surface):
        pass
