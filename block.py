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


def block_main():
    """Рисует все блоки"""
    screen = pg.display.set_mode((1200, 800))
    pg.display.set_caption('Block')
    blocks = []
    k = 28 #Количество типов блоков
    j = (screen_width - block_size*(k-1) - 10*(k-1))/2
    for i in range(28):
        blocks.append(Block(j, screen_height/2 - block_size, i))
        j += 10 + block_size
    run = True
    for block in blocks:
        block.draw_on(screen)
    pg.display.update()
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False


if __name__ == "__main__":
    block_main()
