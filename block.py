import constants
import visual
from constants import *


class Block(visual.DrawableObject):
    def __init__(self, x, y, size, type):
        self.x = x
        self.y = y
        self.size = size
        self.type = type

    def draw_on(self, surface):
        block_surf = None
        if self.type == constants.BlockType.dirt:
            block_surf = constants.BlockImage.dirt
        block_rect = block_surf.get_rect(
            bottomright=(self.size, self.size))
        surface.blit(block_surf, block_rect)

