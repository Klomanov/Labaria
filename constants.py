import pygame as pg

block_size = 30
height = 800
width = 1200

external_world_size = 30
world_size_x = width // block_size + external_world_size  # Ширина карты мира
world_size_y = height // block_size + 5  # Высота карты мира
sky_level = world_size_y - world_size_y // 3  # Уровень неба
perlin_octaves = 2


class BlockType:
    grass = 0
    dirt = 1
    sky = 2


block_images = {BlockType.grass: pg.image.load("textures/tile_grass.jpg"),
                BlockType.dirt: pg.image.load("textures/tile_dirt.png"),
                BlockType.sky: pg.image.load("textures/tile_sky.png"), }
