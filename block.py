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


    def draw_on(self, surface):
        block_surf = block_images[self.type]
        block_surf = pg.transform.scale(block_surf, (block_size, block_size))
        block_rect = block_surf.get_rect(
            center=(self.x, self.y))
        surface.blit(block_surf, block_rect)

