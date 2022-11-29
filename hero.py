import pygame as pg
import constants


class Hero():
    def __init__(self, screen):
        self.screen = screen
        self.animCount = 0

    def static(self, position):
        self.screen.blit(constants.playerStand, (constants.width / 2,
                         constants.height - (position + 1) * constants.block_size))

    def draw_hero(self, event, position):
        if self.animCount + 1 >= 35:
            self.animCount = 0

        if event == 'a':
            self.screen.blit(constants.animLeft[self.animCount // 5], (constants.width / 2,
                             constants.height - (position + 1)*constants.block_size))
            self.animCount += 1
        elif event == 'd':
            self.screen.blit(constants.animRight[self.animCount // 5], (constants.width / 2,
                             constants.height - (position + 1) * constants.block_size))
            self.animCount += 1
        elif event == 'j':
            self.screen.blit(constants.playerJumped, (constants.width / 2,
                             constants.height - (position + 1) * constants.block_size))






