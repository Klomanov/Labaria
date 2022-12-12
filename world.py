import pygame
from perlin_noise import PerlinNoise

import visual
from constants import *
from block import Block
import random
from matplotlib import pyplot as plt


class World:
    def __init__(self, seed):
        self.seed = seed
        self.map = []
        self.vx = 0
        self.vy = 0
        self.__init_landscape()
        self.__init_surface()
        self.__init_stone()
        self.__init_caves()
        self.__make_chunks()

    def __build_tree(self, chunk, bot_x, bot_y, height):
        self.map[bot_y][bot_x] = Block(self.map[bot_y][bot_x].x, self.map[bot_y][bot_x].y, BlockType.tree_bottom)
        for i in range(1, height):
            self.replace_block(chunk, bot_x, bot_y - i, BlockType.tree_middle)
        self.replace_block(chunk, bot_x, bot_y-height, BlockType.tree_top)
        self.replace_block(chunk, bot_x-1, bot_y-height, BlockType.leaves_left_bottom)
        self.replace_block(chunk, bot_x+1, bot_y-height, BlockType.leaves_right_bottom)
        self.replace_block(chunk, bot_x, bot_y-height-1, BlockType.leaves_middle_middle)
        self.replace_block(chunk, bot_x-1, bot_y-height-1, BlockType.leaves_left_middle)
        self.replace_block(chunk, bot_x+1, bot_y-height-1, BlockType.leaves_right_middle)
        self.replace_block(chunk, bot_x, bot_y-height-2, BlockType.leaves_middle_top)
        self.replace_block(chunk, bot_x-1, bot_y-height-2, BlockType.leaves_left_top)
        self.replace_block(chunk, bot_x+1, bot_y-height-2, BlockType.leaves_right_top)

    def __init_caves(self):
        if self.seed == -1:
            noise1 = PerlinNoise(perlin_octaves)
            noise2 = PerlinNoise(perlin_octaves * 2)
        else:
            noise1 = PerlinNoise(perlin_octaves, self.seed)
            noise2 = PerlinNoise(perlin_octaves * 2, self.seed)

        for x in range(world_size_x):
            grass_y = None
            for y in range(world_size_y):
                if self.map[y][x].type == BlockType.grass: grass_y = y
                if grass_y is not None and y >= grass_y:
                    value = noise1([x / world_size_x, y / world_size_y]) + 0.4 * noise2(
                        [x / world_size_x, y / world_size_y])
                    if round(value * 12) == 1:
                        self.map[y][x] = Block(self.map[y][x].x, self.map[y][x].y, block_bg[self.map[y][x].type])

    def __init_landscape(self):
        """
        Инициализирует мир с помощью шума Перлина.
        :return: массив мира
        """

        self.map = []

        for y in range(0, world_size_y):
            self.map.append([])
            for x in range(world_size_x):
                self.map[y].append(Block(block_size * x, block_size * y, BlockType.sky))

        if self.seed == -1:
            noise1 = PerlinNoise(perlin_octaves)
            noise2 = PerlinNoise(perlin_octaves * 8)
        else:
            noise1 = PerlinNoise(perlin_octaves, self.seed)
            noise2 = PerlinNoise(perlin_octaves * 8, self.seed)

        ground_level_noise = []
        for y in range(world_size_y):
            ground_level_noise.append([])
            for x in range(world_size_x):
                value = noise1([x / world_size_x, y / world_size_y]) + 0.3 * noise2(
                    [x / world_size_x, y / world_size_y])
                ground_level_noise[y].append(value)

        # plt.imshow(ground_level_noise, cmap='gray')
        # plt.show()

        self.map.append([])
        for x in range(world_size_x):
            y = round(sky_level - abs(ground_level_noise[0][x] * 15))
            self.map[y][x] = Block(self.map[y][x].x, self.map[y][x].y, BlockType.grass)
            for ny in range(y + 1, world_size_y):
                self.map[ny][x] = Block(self.map[ny][x].x, self.map[ny][x].y, BlockType.dirt)

    def __init_stone(self):
        if self.seed == -1:
            noise1 = PerlinNoise(perlin_octaves)
            noise2 = PerlinNoise(perlin_octaves * 2)
        else:
            noise1 = PerlinNoise(perlin_octaves, self.seed)
            noise2 = PerlinNoise(perlin_octaves * 2, self.seed)

        for x in range(world_size_x):
            grass_y = None
            for y in range(world_size_y):
                if self.map[y][x].type == BlockType.grass: grass_y = y
            value = noise1([x / world_size_x, 1]) + 0.9 * noise2(
                [x / world_size_x, 1])
            stone_y = round(grass_y + 2 + abs(value * 12))
            self.map[stone_y][x] = Block(self.map[stone_y][x].x, self.map[stone_y][x].y, BlockType.stone)
            for ny in range(stone_y + 1, world_size_y):
                self.map[ny][x] = Block(self.map[ny][x].x, self.map[ny][x].y, BlockType.stone)

    def __init_surface(self):
        for x in range(world_size_x):
            for y in range(world_size_y):
                if self.map[y][x].type == BlockType.grass:
                    if random.random() >= 0.97:
                        pass
                        # self.build_tree(x, y-1, random.randint(3, 20))

    def get_block(self, point_x, point_y):
        """
        Получает объект блока по заданной координате
        :param point_y:
        :param point_x:

        :return: Block object
        """
        for chunk in range(len(self.map)):
            for y in range(len(self.map[chunk])):
                for x in range(len(self.map[chunk][y])):
                    if self.map[chunk][y][x].rect.collidepoint((point_x, point_y)):
                        return chunk, x, y

    def replace_block(self, chunk, old_block_x, old_block_y, new_type):
        if old_block_x < 0:
            old_block_x = chunk_size - old_block_x
            chunk -= 1
        if old_block_x > chunk_size:
            old_block_x = old_block_x - chunk_size
            chunk += 1
        self.map[chunk][old_block_y][old_block_x] = Block(self.map[chunk][old_block_y][old_block_x].x,
                                                   self.map[chunk][old_block_y][old_block_x].y, new_type)

    def move(self, vx, vy):
        """Двигает все блоки в соответствии со скоростью"""
        for chunk in self.map:
            for row in chunk:
                for block in row:
                    block.y += round(vy)
                    block.x += round(vx)

    def will_collide_with_rect(self, vx, vy, rect):
        """
        Проверяет столкновение мира с объектом через фрейм c заданной скоростью
        :param vy: скорость по игрек
        :param vx: скорость по икс
        :param rect: коллайдер объекта
        :return: True - если столкнется, False - если нет.
        """
        for chunk in self.map:
            for row in chunk:
                for block in row:
                    if block.rect.move(vx + (0.5 * vx / abs(vx) if vx != 0 else 0),
                                       vy + (0.5 * vy / abs(vy) if vy != 0 else 0)).colliderect(rect) and block.collidable:
                        return True
        return False

    def remove_block(self, chunk, x, y):
        self.replace_block(chunk, x, y, block_bg[self.map[chunk][y][x].type])

    def __make_chunks(self):
        chunk1 = []
        for y in range(world_size_y):
            chunk1.append([])
            for x in range(0, chunk_size):
                chunk1[y].append(self.map[y][x])
        chunk2 = []
        for y in range(world_size_y):
            chunk2.append([])
            for x in range(chunk_size, chunk_size*2):
                chunk2[y].append(self.map[y][x])
        chunk3 = []
        for y in range(world_size_y):
            chunk3.append([])
            for x in range(chunk_size*2, chunk_size*3):
                chunk3[y].append(self.map[y][x])
        self.map = [chunk1, chunk2, chunk3]

    def move_chunk_to_left(self, chunk):
        for row in self.map[chunk]:
            for block in row:
                block.x -= round(3*chunk_size*block_size)

    def move_chunk_to_right(self, chunk):
        for row in self.map[chunk]:
            for block in row:
                block.x += round(3*chunk_size*block_size)


