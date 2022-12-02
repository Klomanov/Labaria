import pygame as pg
from constants import *
import visual


class Hero(visual.DrawableObject):
    def __init__(self):
        self.animCount = 0
        self.y = sky_level
        self.anim_type = AnimationType.static

    def set_animation(self, anim):
        self.anim_type = anim

    def draw_on(self, screen):
        if self.animCount + 1 >= 35:
            self.animCount = 0

        if self.anim_type == AnimationType.left:
            screen.blit(animLeft[self.animCount // 5], (width / 2 - 30,
                                                        height/2 - 135))#числа подогнаны так,чтобы персонаж был примерно в центре
            self.animCount += 1
        elif self.anim_type == AnimationType.right:
            screen.blit(animRight[self.animCount // 5], (width / 2 - 30,
                                                         height/2 - 135)) #числа подогнаны так,чтобы персонаж был примерно в центре
            self.animCount += 1
        elif self.anim_type == AnimationType.jump:
            screen.blit(playerJumped, (width / 2 - 30,
                                       height/2 - 135))#числа подогнаны так,чтобы персонаж был примерно в центре

        elif self.anim_type == AnimationType.static:
            screen.blit(playerStand, (width / 2 - 30,
                                      height/2 - 135))#числа подогнаны так,чтобы персонаж был примерно в центре
# height - (self.y + 1) * block_size