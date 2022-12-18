import pygame
from perlin_noise import PerlinNoise

import visual
from constants import *
from block import Block
import random
from matplotlib import pyplot as plt
import time
import pickle


class World:
    def __init__(self, seed=None, file_name=None):
        self.map = []
        self.vx = 0
        self.vy = 0
        self.seed = seed
        if seed is None:
            self.load_world(file_name)
        else:
            self.create_new_world()

    def load_world(self, name: str):
        file = open(f'saves/{name}', 'rb')
        map_converted = pickle.load(file)[0].pickled_map
        for i in range(len(map_converted)):
            self.map.append([])
            for j in range(len(map_converted[i])):
                self.map[i].append([])
                for k in range(len(map_converted[i][j])):
                    self.map[i][j].append(
                        Block(map_converted[i][j][k].x, map_converted[i][j][k].y, map_converted[i][j][k].type))
        file.close()

    def create_new_world(self):
        self.__init_sky()
        self.__init_landscape()
        self.__init_stone()
        self.__init_caves()
        self.__init_surface()
        self.__init_underground_filling()
        self.__init_bedrock()

    def generate_perlin_noise(self, dim, layers_num, octaves_arr, coefficient_arr):
        """
        Генерирует зацикленный dim-мерный шум Перлина по чанкам
        :param dim: 2-3 размерность
        :param layers_num: количество слоев шума
        :param octaves_arr: зернистость каждого слоя
        :param coefficient_arr: степень влияния каждого слоя в виде коэф.
        :return: массив из 4 чанков с шумом Перлина
        """
        noises = []
        if self.seed == -1:
            for i in range(layers_num):
                noises.append(PerlinNoise(perlin_octaves * octaves_arr[i]))
        else:
            for i in range(layers_num):
                noises.append(PerlinNoise(perlin_octaves * octaves_arr[i], seed=self.seed))
        perlin_map = []
        if dim == 2:
            perlin_map = [[], [], [], []]
            for x in range(chunk_size):
                value = noises[0]([x / chunk_size, 0]) * coefficient_arr[0]
                for i in range(1, len(noises)):
                    value += noises[i]([x / chunk_size, 0]) * coefficient_arr[i]
                perlin_map[0].append(value)
            for x in range(chunk_size):
                value = noises[0]([1, x / chunk_size]) * coefficient_arr[0]
                for i in range(1, len(noises)):
                    value += noises[i]([x / chunk_size, 0]) * coefficient_arr[i]
                perlin_map[1].append(value)
            for x in range(chunk_size):
                value = noises[0]([1 - x / chunk_size, 1]) * coefficient_arr[0]
                for i in range(1, len(noises)):
                    value += noises[i]([x / chunk_size, 0]) * coefficient_arr[i]
                perlin_map[2].append(value)
            for x in range(chunk_size):
                value = noises[0]([0, 1 - x / chunk_size]) * coefficient_arr[0]
                for i in range(1, len(noises)):
                    value += noises[i]([x / chunk_size, 0]) * coefficient_arr[i]
                perlin_map[3].append(value)
        if dim == 3:
            perlin_map = [[], [], [], []]
            for y in range(world_size_y):
                perlin_map[0].append([])
                for x in range(chunk_size):
                    value = noises[0]([x / chunk_size, y / world_size_y, 0, ]) * coefficient_arr[0]
                    for i in range(1, len(noises)):
                        value += noises[i]([x / chunk_size, y / world_size_y, 0, ]) * coefficient_arr[i]
                    perlin_map[0][y].append(value)
            for y in range(world_size_y):
                perlin_map[1].append([])
                for x in range(chunk_size):
                    value = noises[0]([1, y / world_size_y, x / chunk_size, ]) * coefficient_arr[0]
                    for i in range(1, len(noises)):
                        value += noises[i]([1, y / world_size_y, x / chunk_size, ]) * coefficient_arr[i]
                    perlin_map[1][y].append(value)
            for y in range(world_size_y):
                perlin_map[2].append([])
                for x in range(chunk_size):
                    value = noises[0]([1 - x / chunk_size, y / world_size_y, 1]) * coefficient_arr[0]
                    for i in range(1, len(noises)):
                        value += noises[i]([1 - x / chunk_size, y / world_size_y, 1]) * coefficient_arr[i]
                    perlin_map[2][y].append(value)
            for y in range(world_size_y):
                perlin_map[3].append([])
                for x in range(chunk_size):
                    value = noises[0]([0, y / world_size_y, 1 - x / chunk_size]) * coefficient_arr[0]
                    for i in range(1, len(noises)):
                        value += noises[i]([0, y / world_size_y, 1 - x / chunk_size]) * coefficient_arr[i]
                    perlin_map[3][y].append(value)
            # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
            # ax1.imshow(perlin_map[0], cmap='gray')
            # ax2.imshow(perlin_map[1], cmap='gray')
            # ax3.imshow(perlin_map[2], cmap='gray')
            # ax4.imshow(perlin_map[3], cmap='gray')
            # plt.show()
        return perlin_map

    def __build_tree(self, chunk, bot_x, bot_y, height):
        leaves = [[BlockType.leaves_left_bottom, BlockType.leaves_middle_bottom, BlockType.leaves_right_bottom],
                  [BlockType.leaves_left_middle, BlockType.leaves_middle_middle, BlockType.leaves_right_middle],
                  [BlockType.leaves_left_top, BlockType.leaves_middle_top, BlockType.leaves_right_top]]
        self.map[chunk][bot_y][bot_x] = Block(self.map[chunk][bot_y][bot_x].x, self.map[chunk][bot_y][bot_x].y,
                                              BlockType.tree_bottom)
        for i in range(1, height):
            self.__replace_block(chunk, bot_x, bot_y - i, BlockType.tree_middle)
        for y in range(3):
            for x in range(3):
                c = chunk
                nx = bot_x + x - 1
                if nx < 0:
                    c -= 1
                    nx += chunk_size
                elif nx >= chunk_size:
                    c += 1
                    nx -= chunk_size
                    if c == chunk_num: c = 0
                self.__replace_block(c, nx, bot_y - height - y, leaves[y][x])

    def __init_caves(self):

        caves = self.generate_perlin_noise(3, 2, [1, 2], [1, 0.3])

        for z in range(chunk_num):
            for x in range(chunk_size):
                grass_y = None
                for y in range(world_size_y):
                    if self.map[z][y][x].type == BlockType.grass: grass_y = y
                    if grass_y is not None and y >= grass_y:
                        value = abs(caves[z][y][x])
                        if value * caves_frequency * 20 <= 1:
                            self.map[z][y][x] = Block(self.map[z][y][x].x, self.map[z][y][x].y,
                                                      block_bg[self.map[z][y][x].type])

    def __init_sky(self):
        for chunk in range(chunk_num):
            self.map.append([])
            for y in range(world_size_y):
                self.map[chunk].append([])
                for x in range(chunk * chunk_size, (chunk + 1) * chunk_size):
                    self.map[chunk][y].append(Block(block_size * x, block_size * y, BlockType.sky))

    def __init_landscape(self):
        """
        Инициализирует первичный ландшафт с помощью шума Перлина.
        :return: массив мира
        """
        ground_level_noise = self.generate_perlin_noise(2, 2, [1, 3], [1, 0.3])

        # plt.imshow(ground_level_noise, cmap='gray')
        # plt.show()

        for z in range(chunk_num):
            for x in range(chunk_size):
                y = round(sky_level - abs(ground_level_noise[z][x] * 15))
                self.map[z][y][x] = Block(self.map[z][y][x].x, self.map[z][y][x].y, BlockType.grass)
                for ny in range(y + 1, world_size_y):
                    self.map[z][ny][x] = Block(self.map[z][ny][x].x, self.map[z][ny][x].y, BlockType.dirt)

    def __init_stone(self):
        stone_level_noise = self.generate_perlin_noise(2, 2, [1, 2], [1, 0.9])

        for z in range(chunk_num):
            for x in range(chunk_size):
                grass_y = None
                for y in range(world_size_y):
                    if self.map[z][y][x].type == BlockType.grass: grass_y = y
                stone_y = round(grass_y + 2 + abs(stone_level_noise[z][x] * 12))
                self.map[z][stone_y][x] = Block(self.map[z][stone_y][x].x, self.map[z][stone_y][x].y, BlockType.stone)
                for ny in range(stone_y + 1, world_size_y):
                    self.map[z][ny][x] = Block(self.map[z][ny][x].x, self.map[z][ny][x].y, BlockType.stone)

    def __init_surface(self):
        decorations_surface = [BlockType.dec_grass1, BlockType.dec_grass2, BlockType.dec_grass3, BlockType.dec_grass4,
                               BlockType.dec_mushroom_brown, BlockType.dec_mushroom_red, ]
        for z in range(chunk_num):
            for y in range(world_size_y):
                for x in range(chunk_size):
                    if self.map[z][y][x].type == BlockType.grass:
                        if random.random() >= 0.9 / tree_frequency:
                            height = random.randint(3, 15)
                            if self.__can_place_tree(z, x, y - 1, height):
                                self.__build_tree(z, x, y - 1, height)
                        if random.random() >= 0.8 / decorations_frequency and self.map[z][y - 1][
                            x].type == BlockType.sky:
                            self.__replace_block(z, x, y - 1,
                                               decorations_surface[random.randint(0, len(decorations_surface) - 1)])

    def __init_underground_filling(self):
        decorations_underground = [BlockType.dec_rock, BlockType.dec_rock_moss]
        for z in range(chunk_num):
            for y in range(world_size_y - 1):
                for x in range(chunk_size):
                    if self.map[z][y][x].type == BlockType.bg_stone:
                        if random.random() >= 0.8 / decorations_frequency and self.map[z][y + 1][
                            x].type == BlockType.stone:
                            self.__replace_block(z, x, y,
                                               decorations_underground[
                                                   random.randint(0, len(decorations_underground) - 1)])

    def __init_bedrock(self):
        bedrock_level_noise = self.generate_perlin_noise(2, 1, [0.5], [1])

        # plt.imshow(ground_level_noise, cmap='gray')
        # plt.show()

        for z in range(chunk_num):
            for x in range(chunk_size):
                y = round(bedrock_level - abs(bedrock_level_noise[z][x] * 15))
                self.map[z][y][x] = Block(self.map[z][y][x].x, self.map[z][y][x].y, BlockType.bedrock)
                for ny in range(y + 1, world_size_y):
                    self.map[z][ny][x] = Block(self.map[z][ny][x].x, self.map[z][ny][x].y, BlockType.bedrock)

    def __can_place_tree(self, chunk, bot_x, bot_y, height):
        for i in range(1, height):
            if self.map[chunk][bot_y - i][bot_x].type != BlockType.sky:
                return False
        for y in range(3):
            for x in range(3):
                c = chunk
                nx = bot_x + x - 1
                if nx < 0:
                    c -= 1
                    nx += chunk_size
                elif nx >= chunk_size:
                    c += 1
                    nx -= chunk_size
                    if c == chunk_num: c = 0
                if self.map[c][bot_y - height - y][nx].type != BlockType.sky:
                    return False
        return True

    def get_block(self, point_x, point_y):
        """
        Получает объект блока по заданной координате
        :param point_y:
        :param point_x:

        :return: Block object
        """
        for chunk in range(len(self.map)):
            if visual.is_chunk_on_screen(self.map[chunk]):
                for y in range(len(self.map[chunk])):
                    for x in range(len(self.map[chunk][y])):
                        if visual.is_block_on_screen(self.map[chunk][y][x]):
                            if self.map[chunk][y][x].rect.collidepoint((point_x, point_y)):
                                return chunk, x, y
        return None, None, None

    def __replace_block(self, chunk, old_block_x, old_block_y, new_type):
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
            if visual.is_chunk_on_screen(chunk):
                for row in chunk:
                    for block in row:
                        if visual.is_block_on_screen(block):
                            if block.rect.move(vx + (0.5 * vx / abs(vx) if vx != 0 else 0),
                                               vy + (0.5 * vy / abs(vy) if vy != 0 else 0)).colliderect(
                                rect) and block.collidable:
                                return True
        return False

    def remove_block(self, chunk, x, y):
        self.__replace_block(chunk, x, y, block_bg[self.map[chunk][y][x].type])

    def place_block(self, chunk, x, y, new_type):
        self.__replace_block(chunk, x, y, new_type)

    def move_right_chunk_to_left(self):
        for row in self.map[-1]:
            for block in row:
                block.x -= round(chunk_num * chunk_size * block_size)
        c = self.map[-1]
        self.map.pop(chunk_num - 1)
        self.map.insert(0, c)

    def move_left_chunk_to_right(self):
        for row in self.map[0]:
            for block in row:
                block.x += round(chunk_num * chunk_size * block_size)
        c = self.map[0]
        self.map.pop(0)
        self.map.insert(chunk_num - 1, c)
