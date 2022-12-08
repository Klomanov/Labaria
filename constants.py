import pygame as pg

block_size = 30
height = 800
width = 1200
font_size = 24

g = 1  # ускорение свободного падения

# Ширина карты мира
external_world_size = 100
world_size_x = width // block_size + external_world_size  # Ширина карты мира
world_size_y = height // block_size + 50  # Высота карты мира
sky_level = world_size_y - world_size_y // 3  # s Уровень неба

hero_spawn_x = width // 2  # Место спавна героя
hero_spawn_y = height // 2
hero_width = 1.75 * block_size  # Геометрические размеры героя
hero_height = 2.15 * block_size
hero_speed = 3  # Кинематические свойства героя (в целых числах все нужно указывать)
hero_jump_power = 20

perlin_octaves = 1.5  # Зернистость генерации мира


class BlockType:
    grass = 0
    dirt = 1
    sky = 2
    bg_dirt = 3
    stone = 4
    bg_stone = 5


class Animations:
    left = [pg.transform.scale(pg.image.load("animation/character_male_left_walk0.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk1.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk2.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk3.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk4.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk5.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk6.png"), (hero_width, hero_height)),
            pg.transform.scale(pg.image.load("animation/character_male_left_walk7.png"), (hero_width, hero_height))]
    right = [pg.transform.scale(pg.image.load("animation/character_male_right_walk0.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk1.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk2.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk3.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk4.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk5.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk6.png"), (hero_width, hero_height)),
             pg.transform.scale(pg.image.load("animation/character_male_right_walk7.png"), (hero_width, hero_height))]
    jump_right = [pg.transform.scale(pg.image.load("animation/character_male_right_jump.png"), (hero_width, hero_height))]
    jump_left = [pg.transform.scale(pg.image.load("animation/character_male_left_jump.png"), (hero_width, hero_height))]
    static = [pg.transform.scale(pg.image.load("animation/character_male_idle.png"), (hero_width, hero_height))]
    break_right = [pg.transform.scale(pg.image.load("animation/character_male_right_kick1.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick1.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick2.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick2.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick3.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick3.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick4.png"), (hero_width, hero_height)),
                   pg.transform.scale(pg.image.load("animation/character_male_right_kick4.png"), (hero_width, hero_height))]
    break_left = [pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick2.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick2.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick3.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick3.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick4.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_left_kick4.png"), (hero_width, hero_height))]
    break_down = [pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick2.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick3.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick3.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick4.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick5.png"), (hero_width, hero_height)),
                  pg.transform.scale(pg.image.load("animation/character_male_down_kick6.png"), (hero_width, hero_height))]


block_images = {BlockType.grass: pg.image.load("textures/tile_grass.jpg"),
                BlockType.dirt: pg.image.load("textures/tile_dirt.png"),
                BlockType.sky: pg.image.load("textures/tile_sky.png"),
                BlockType.bg_dirt: pg.image.load("textures/tile_bg_dirt.png"),
                BlockType.stone: pg.image.load("textures/tile_stone.png"),
                BlockType.bg_stone: pg.image.load("textures/tile_bg_stone.png")}

block_collisions = {BlockType.grass: True,
                    BlockType.dirt: True,
                    BlockType.sky: False,
                    BlockType.bg_dirt: False,
                    BlockType.stone: True,
                    BlockType.bg_stone: False,
                    }

start_img_off = pg.image.load("menu/button_start_off.png")
start_img_on = pg.image.load("menu/button_start_on.png")
exit_img_on = pg.image.load("menu/button_exit_on.png")
exit_img_off = pg.image.load("menu/button_exit_off.png")
load_save_on = pg.image.load("menu/button_load_save_on.png")
load_save_off = pg.image.load("menu/button_load_save_off.png")
LABaria_pict = pg.image.load("menu/LABaria.png")


