import pygame as pg
import visual
from constants import *


class Resource:
    def __init__(self, name, image):
        self.name = name
        self.amount = 0
        self.image = pg.transform.scale(image, (block_size, block_size))


class Inventory(visual.DrawableObject):
    def __init__(self, screen):
        self.screen = screen
        self.whole_inventory = []
        for name in resource:
            self.whole_inventory.append(Resource(name, resource_images[name]))

    def increase(self, name):
        self.whole_inventory[name].amount += 1

    def print_text(self, amount, x, y):
        f = pg.font.Font(None, font_size)
        f = f.render(amount, True, (180, 0, 0))
        self.screen.blit(f, (x, y))

    def draw_on(self, screen):
        x = (screen_width - 290)/2 + 10
        y = screen_height - 140 + 10
        side = 60
        step = 70

        pg.draw.rect(screen, (182, 195, 206), (x - 10, y - 10, 290, 80))

        for cell in self.whole_inventory:
            pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            if cell.amount != 0:
                screen.blit(cell.image, (x + side/2 - 18, y + side/2 - 18))
                self.print_text(str(cell.amount), x + side/2 - 5, y + 0.75*side)
            x += step








