import pygame as pg


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update_screen(self, world, hero, inventory):
        """
        Рисует все объекты на экране и обновляет его
        :param inventory:
        :param world:
        :param hero:
        :return:
        """
        self.screen.fill((0, 0, 0))
        for chunk in world:
            for row in chunk:
                for block in row:
                    block.draw_on(self.screen)
        hero.draw_on(self.screen)
        inventory.draw_on(self.screen)
        pg.display.update()


class DrawableObject:
    def draw_on(self, surface):
        pass
