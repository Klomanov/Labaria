import constants
import visual
from constants import *


class Block(visual.DrawableObject):
    def __init__(self, x, y, type, size=block_size):
        self.x = x
        self.y = y
        self.size = size
        self.type = type
        self.collidable = block_collisions.get(type)
        self.image = pg.transform.scale(block_images[self.type], (block_size, block_size))
        self.bg_image = pg.transform.scale(block_images[block_bg[type]], (block_size, block_size))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.breaking_time = block_breaking_time[self.type]

    def draw_on(self, surface):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.bg_image, self.rect)
        surface.blit(self.image, self.rect)

    def set_transparency_level(self, degree):
        """

        :param degree: уровень прозрачности (от 0 до 1)
        :return:
        """
        self.image.set_alpha(255 - degree*255)

