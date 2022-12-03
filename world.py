import pygame
from perlin_noise import PerlinNoise
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
        self.init_world()

    def init_world(self):
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
            noise2 = PerlinNoise(perlin_octaves * 3)
        else:
            noise1 = PerlinNoise(perlin_octaves, self.seed)
            noise2 = PerlinNoise(perlin_octaves * 3, self.seed)

        ground_level_noise = []
        for y in range(world_size_y):
            ground_level_noise.append([])
            for x in range(world_size_x):
                value = noise1([x / world_size_x, y / world_size_y]) + 0.8 * noise2(
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

    def get_block(self, x, y):
        """
        Получает объект блока по заданной координате
        :param x:
        :param y:
        :return: Block object
        """
        for row in self.map:
            for block in row:
                if block.rect.collidepoint((x, y)):
                    return block

    def move(self):
        """Двигает все блоки в соответствии со скоростью"""
        for row in self.map:
            for block in row:
                block.y += self.vy
                block.x += self.vx

    def will_collide_with_rect(self, vx, vy, rect):
        """
        Проверяет столкновение мира с объектом через фрейм c заданной скоростью
        :param vy: скорость по игрек
        :param vx: скорость по икс
        :param rect: коллайдер объекта
        :return: True - если столкнется, False - если нет.
        """
        for row in self.map:
            for block in row:
                if block.rect.move(vx, vy).colliderect(rect) and block.collidable:
                    return True
        return False

