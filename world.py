import pygame
from perlin_noise import PerlinNoise
from constants import *
from block import Block
import random
from matplotlib import pyplot as plt

"""Осуществляет движение мира"""

world_movement_speed_y = 0 #переменная, которая отвечает за скорость вертикального движения мира
jump = False #находится персонаж в прыжке или нет


def init_world(seed=-1):
    """
    Инициализирует мир с помощью шума Перлина.
    :return: массив мира
    """
    world = []

    for y in range(0, world_size_y):
        world.append([])
        for x in range(world_size_x):
            world[y].append(Block(block_size * x, block_size * y, BlockType.sky))

    if seed == -1:
        noise1 = PerlinNoise(perlin_octaves)
        noise2 = PerlinNoise(perlin_octaves*3)
    else:
        noise1 = PerlinNoise(perlin_octaves, seed)
        noise2 = PerlinNoise(perlin_octaves*3, seed)

    ground_level_noise = []
    for y in range(world_size_y):
        ground_level_noise.append([])
        for x in range(world_size_x):
            value = noise1([x / world_size_x, y / world_size_y]) + 0.8*noise2([x / world_size_x, y / world_size_y])
            ground_level_noise[y].append(value)

    plt.imshow(ground_level_noise, cmap='gray')
    plt.show()

    world.append([])
    for x in range(world_size_x):
        y = round(sky_level - abs(ground_level_noise[0][x] * 15))
        world[y][x] = Block(world[y][x].x, world[y][x].y, BlockType.grass)
        for ny in range(y+1, world_size_y):
            world[ny][x] = Block(world[ny][x].x, world[ny][x].y, BlockType.dirt)

    return world


def world_move_left(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for row in world:
        for block in row:
            block.x -= 1


def world_move_right(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for row in world:
        for block in row:
            block.x += 1


def world_jump(world):
    """Функция, которая осуществляет прыжок"""
    global world_movement_speed_y, jump
    if world_movement_speed_y == 0 and jump == False:
        world_movement_speed_y = 6.5
    elif world_movement_speed_y > -7:
        for row in world:
            for block in row:
                block.y += world_movement_speed_y
        world_movement_speed_y -= 0.5
    elif world_movement_speed_y == -7:
        world_movement_speed_y = 0
        jump = False


def world_move_general(world):
    """Функция, которая осуществляет движение мира с помощью других функций в world_move.py"""
    global jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        world_move_right(world)
    if keys[pygame.K_d]:
        world_move_left(world)
    if keys[pygame.K_SPACE] and jump == False:
        world_jump(world)
        jump = True
    elif jump:
        world_jump(world)


def world_move_down(world):
    """Пока что ненужная функция"""
    for strings in world:
        for block in strings:
            block.y += 1


def world_move_up(world):
    """Пока что ненужная функция"""
    for strings in world:
        for block in strings:
            block.y -= 1
