import pygame
from constants import *
from world import *



class Physic_process:
    def __init__(self, gravconst):
        self.g = gravconst
        self.world_movement_speed_y = 0
        self.world_movement_speed_x = 0

    def gravitation(self, world):
        if not check_block(world):
            self.world_movement_speed_y += self.g
        else:
            self.world_movement_speed_y = 0

    def world_move(self, world):
        for row in world:
            for block in row:
                block.y -= self.world_movement_speed_y
                block.x += self.world_movement_speed_x

