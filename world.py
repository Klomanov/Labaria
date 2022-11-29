import pygame as pg
from perlin_noise import PerlinNoise
from constants import *
from block import Block
import random

"""Осуществляет движение мира"""


def init_world(seed=-1):
    """
    Инициализирует мир в три этапа. Небо, трава, земля
    :return: массив мира
    """
    world = []

    for y in range(0, world_size_y):
        world.append([])
        for x in range(world_size_x):
            world[y].append(Block(block_size * x, block_size * y, BlockType.sky))

    if seed == -1:
        noise = PerlinNoise(perlin_octaves)
    else:
        noise = PerlinNoise(perlin_octaves, seed)

    ground_level_noise = []
    for y in range(world_size_y):
        ground_level_noise.append([])
        for x in range(world_size_x):
            ground_level_noise[y].append(noise([x / world_size_x, y / world_size_y]))
    world.append([])
    for x in range(world_size_x):
        y = round(sky_level - abs(ground_level_noise[0][x] * 10))
        world[y][x] = Block(world[y][x].x, world[y][x].y, BlockType.grass)
        for ny in range(y+1, world_size_y):
            world[ny][x] = Block(world[ny][x].x, world[ny][x].y, BlockType.dirt)

    return world


def world_move_left(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for type_block in world:
        for block in type_block:
            block.x -= 1


def world_move_right(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for type_block in world:
        for block in type_block:
            block.x += 1


def world_move_down(world):
    """Пока что ненужная функция"""
    for type_block in world:
        for block in type_block:
            block.y += 1


def world_move_up(world):
    """Пока что ненужная функция"""
    for type_block in world:
        for block in type_block:
            block.y -= 1
