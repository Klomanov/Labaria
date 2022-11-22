import pygame as pg


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, figures, ui):
        self.screen.fill((0, 0, 0))
        for figure in figures:
            figure.draw_on(self.screen)
        if ui is not None:
            ui.blit()
            ui.update()
        pg.display.update()


class DrawableObject:
    def draw_on(self, surface):
        pass
