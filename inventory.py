import pygame as pg
import pygame.mouse
import pickle
import visual
from constants import *


class Resource:

    def __init__(self, name, amount=0):
        self.surname = resource_surnames[name]
        self.image = resource_images[name]
        self.amount = amount


class Inventory(visual.DrawableObject):

    def __init__(self, screen, name=None):
        self.screen = screen
        self.resources = {}
        if name is not None:
            self.load_resources(name)
        self.panel = 4
        self.flag = False

    def load_resources(self, name):
        file = open(f'saves/{name}', 'rb')
        resources = pickle.load(file)[1]
        for name, resource in resources.items():
            self.resources[name] = Resource(name, resource[1])
        file.close()

    def add_resource(self, name):
        self.resources[name] = Resource(name)

    def delete_resource(self, name):
        if name in self.resources:
            del self.resources[name]

    def increase(self, name):
        if name not in self.resources:
            self.add_resource(name)
        self.resources[name].amount += 1

    def decrease(self, name):
        self.resources[name].amount -= 1
        if self.resources[name].amount == 0:
            self.delete_resource(name)

    def print_text(self, amount, x, y):
        f = pg.font.Font('DePixel/DePixelBreit.ttf', font_size)
        f = f.render(amount, True, (180, 0, 0))
        self.screen.blit(f, (x, y))

    def lighting(self, screen, x, y, side):
        pg.draw.rect(screen, (2, 215, 227), (x, y, side, side))

    def draw_on(self, screen):
        full = 0
        x = (screen_width - 290) / 2 + 10
        y = screen_height - 140 + 10
        side = 60
        step = 70

        pg.draw.rect(screen, (182, 195, 206), (x - 10, y - 10, 290, 80))

        for name, resource in self.resources.items():
            pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            if pg.key.get_pressed()[keys[full]]:
                self.lighting(screen, x, y, side)
            if resource.amount != 0:
                screen.blit(resource.image, (x + side / 2 - 18, y + side / 2 - 18))
                self.print_text(str(resource.amount), x + side / 2 - 5, y + 0.75 * side)
            x += step
            full += 1
            if full >= 3:
                pass

        for i in range(4 - full):
            if i != (3 - full):
                pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
                x += step
            else:
                pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
                screen.blit(plus, (x, y))

        click = pygame.mouse.get_pressed()
        if click[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] > 675) and (pos[0] < 735) and (pos[1] > 670) and (pos[1] < 730) and not self.flag:
                self.flag = True
        if self.flag:
            self.draw_inventory(screen)

    def draw_inventory(self, screen):
        full = 0
        x = (screen_width - 630) / 2 + 30
        y = screen_height - 600 + 30
        side = 120
        step = 150

        pg.draw.rect(screen, (182, 195, 206), (x - 30, y - 30, 630, 330))
        screen.blit(cross, (x - 30 + step*4, y - 30, 30, 30))

        for name, resource in self.resources.items():
            pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            if pg.key.get_pressed()[keys[full]]:
                self.lighting(screen, x, y, side)
            if resource.amount != 0:
                screen.blit(resource.image, (x + side / 2 - 18, y + side / 2 - 50))
                self.print_text(str(resource.surname), x + side / 2 - 50, y + side / 2 + 10)
                self.print_text('Amount: ' + str(resource.amount), x + side / 2 - 50, y + side / 2 + 30)
            x += step
            if x == (screen_width - 630) / 2 + 30 + 4*150:
                x = (screen_width - 630) / 2 + 30
                y += step
            full += 1

        for i in range(8 - full):
            pg.draw.rect(screen, (200, 215, 227), (x, y, side, side))
            x += step
            if x == (screen_width - 630) / 2 + 30 + 4*150:
                x = (screen_width - 630) / 2 + 30
                y += step

        click = pygame.mouse.get_pressed()
        if click[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] > 885) and (pos[0] < 915) and (pos[1] > 200) and (pos[1] < 230) and self.flag:
                self.flag = False


def inventory_main():
    """Рисует инвентарь, добавляет один блок земли. Инвентарь можно открыть."""
    pg.font.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Inventory')
    inventory = Inventory(screen)
    inventory.increase(BlockType.dirt)
    run = True
    while run:
        screen.fill((0, 0, 0))
        inventory.draw_on(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    inventory_main()
