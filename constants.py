import pygame as pg

block_size = 30
height = 800
width = 1200

external_world_size = 30
world_size_x = width // block_size + external_world_size  # Ширина карты мира
world_size_y = height // block_size + 5  # Высота карты мира
sky_level = world_size_y - world_size_y // 3  #s Уровень неба
perlin_octaves = 1.5


class BlockType:
    grass = 0
    dirt = 1
    sky = 2


class AnimationType:
    left = "left"
    right = "right"
    jump = "jump"
    static = "static"


block_images = {BlockType.grass: pg.image.load("textures/tile_grass.jpg"),
                BlockType.dirt: pg.image.load("textures/tile_dirt.png"),
                BlockType.sky: pg.image.load("textures/tile_sky.png"), }

playerStand = pg.image.load("animation/character_male_idle.png")


animRight = [pg.image.load("animation/character_male_right_walk0.png"),
             pg.image.load("animation/character_male_right_walk1.png"),
             pg.image.load("animation/character_male_right_walk2.png"),
             pg.image.load("animation/character_male_right_walk3.png"),
             pg.image.load("animation/character_male_right_walk4.png"),
             pg.image.load("animation/character_male_right_walk5.png"),
             pg.image.load("animation/character_male_right_walk6.png"),
             pg.image.load("animation/character_male_right_walk7.png")]

animLeft = [pg.image.load("animation/character_male_left_walk0.png"),
            pg.image.load("animation/character_male_left_walk1.png"),
            pg.image.load("animation/character_male_left_walk2.png"),
            pg.image.load("animation/character_male_left_walk3.png"),
            pg.image.load("animation/character_male_left_walk4.png"),
            pg.image.load("animation/character_male_left_walk5.png"),
            pg.image.load("animation/character_male_left_walk6.png"),
            pg.image.load("animation/character_male_left_walk7.png")]

playerJumped = pg.image.load("animation/character_maleAdventurer_jump.png")