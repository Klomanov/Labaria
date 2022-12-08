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
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.breakable = block_breakable[self.type]

    def draw_on(self, surface):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, self.rect)

