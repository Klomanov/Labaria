import pygame as pg
import visual
from constants import *


class Resource:
    def __init__(self, name, image_path):
        self.name = name
        self.amount = 0
        self.image = pg.image.load(image_path)


class Inventory(visual.DrawableObject):
    def __init__(self, screen):
        self.screen = screen
        self.resources = {
            "dirt": Resource("dirt", "textures/dirt_inventory.png"),
            "grass": Resource("glass", "textures/tile_grass.jpg"),
            "sky": Resource("sky", "textures/tile_sky.png")
        }
        #self.inventory_panel = [None] * 4
        self.whole_inventory = [None] * 4

    def increase(self, name):
        try:
            self.resources[name].amount += 1
        except KeyError:
            print("Error increasing")
        self.update_whole()

    def update_whole(self):
        for name, resource in self.resources.items():
            if resource.amount != 0 and resource not in self.whole_inventory:
                self.whole_inventory.insert(self.whole_inventory.index(None), resource)
                self.whole_inventory.remove(None)

    def print_text(self, amount, x, y):
        f = pg.font.Font(None, font_size)
        f = f.render(amount, True, (180, 0, 0))
        self.screen.blit(f, (x, y))

    def draw_on(self, screen):
        x = (width - 290)/2 + 10
        y = height - 140 + 10
        side = 60
        step = 70

        pg.draw.rect(screen, (182, 195, 206), (x - 10, y - 10, 290, 80))

        for cell in self.whole_inventory:
            pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            if cell is not None:
                screen.blit(cell.image, (x + side/2 - 18, y + side/2 - 18))
                self.print_text(str(cell.amount), x + side/2 - 5, y + 0.75*side)
            x += step








