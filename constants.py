import pygame as pg

block_size = 30
screen_height = 800
screen_width = 1200
font_size = 24

g = 1  # ускорение свободного падения

# Ширина карты мира
external_world_size = 100
world_size_x = screen_width // block_size + external_world_size  # Ширина карты мира
world_size_y = screen_height // block_size + 50  # Высота карты мира
sky_level = world_size_y - world_size_y // 3  # s Уровень неба

hero_spawn_x = screen_width // 2  # Место спавна героя
hero_spawn_y = screen_height // 2
hero_width = 1.75 * block_size  # Геометрические размеры героя
hero_height = 2 * block_size
hero_speed = 3  # Кинематические свойства героя (в целых числах все нужно указывать)
hero_jump_power = 20
hero_dig_range = 2.3 * block_size

perlin_octaves = 1.5  # Зернистость генерации мира


class BlockType:
    grass = 0
    dirt = 1
    sky = 2
    bg_dirt = 3
    stone = 4
    bg_stone = 5
    tree_bottom = 6
    tree_middle = 7
    tree_top = 8
    leaves_left_bottom = 9
    leaves_middle_bottom = 10
    leaves_right_bottom = 11
    leaves_left_middle = 12
    leaves_middle_middle = 13
    leaves_right_middle = 14
    leaves_left_top = 15
    leaves_middle_top = 16
    leaves_right_top = 17


block_images = {BlockType.grass: pg.image.load("textures/tile_grass.jpg"),
                BlockType.dirt: pg.image.load("textures/tile_dirt.png"),
                BlockType.sky: pg.image.load("textures/tile_sky.png"),
                BlockType.bg_dirt: pg.image.load("textures/tile_bg_dirt.png"),
                BlockType.stone: pg.image.load("textures/tile_stone.png"),
                BlockType.bg_stone: pg.image.load("textures/tile_bg_stone.png"),
                BlockType.tree_bottom: pg.image.load("textures/tree/tile_tree_bottom.png"),
                BlockType.tree_middle: pg.image.load("textures/tree/tile_tree_middle.png"),
                BlockType.tree_top: pg.image.load("textures/tree/tile_tree_top.png"),
                BlockType.leaves_left_bottom: pg.image.load("textures/tree/tile_leaves_left_bottom.png"),
                BlockType.leaves_middle_bottom: pg.image.load("textures/tree/tile_leaves_middle_bottom.png"),
                BlockType.leaves_right_bottom: pg.image.load("textures/tree/tile_leaves_right_bottom.png"),
                BlockType.leaves_left_middle: pg.image.load("textures/tree/tile_leaves_left_middle.png"),
                BlockType.leaves_middle_middle: pg.image.load("textures/tree/tile_leaves_middle_middle.png"),
                BlockType.leaves_right_middle: pg.image.load("textures/tree/tile_leaves_right_middle.png"),
                BlockType.leaves_left_top: pg.image.load("textures/tree/tile_leaves_left_top.png"),
                BlockType.leaves_middle_top: pg.image.load("textures/tree/tile_leaves_middle_top.png"),
                BlockType.leaves_right_top: pg.image.load("textures/tree/tile_leaves_right_top.png"), }

block_breaking_time = {BlockType.grass: 0.5,  # Время в секундах на ломание блока
                       BlockType.dirt: 0.5,
                       BlockType.stone: 1,
                       BlockType.bg_dirt: None,
                       BlockType.sky: None,
                       BlockType.bg_stone: None,
                       BlockType.tree_bottom: 0.75,
                       BlockType.tree_middle: 0.75,
                       BlockType.tree_top: 0.75,
                       BlockType.leaves_left_bottom: 0.2,
                       BlockType.leaves_middle_bottom: 0.2,
                       BlockType.leaves_right_bottom: 0.2,
                       BlockType.leaves_left_middle: 0.2,
                       BlockType.leaves_middle_middle: 0.2,
                       BlockType.leaves_right_middle: 0.2,
                       BlockType.leaves_left_top: 0.2,
                       BlockType.leaves_middle_top: 0.2,
                       BlockType.leaves_right_top: 0.2,
                       }

block_collisions = {BlockType.grass: True,
                    BlockType.dirt: True,
                    BlockType.sky: False,
                    BlockType.bg_dirt: False,
                    BlockType.stone: True,
                    BlockType.bg_stone: False,
                    BlockType.tree_bottom: False,
                    BlockType.tree_middle: False,
                    BlockType.tree_top: False,
                    BlockType.leaves_left_bottom: False,
                    BlockType.leaves_middle_bottom: False,
                    BlockType.leaves_right_bottom: False,
                    BlockType.leaves_left_middle: False,
                    BlockType.leaves_middle_middle: False,
                    BlockType.leaves_right_middle: False,
                    BlockType.leaves_left_top: False,
                    BlockType.leaves_middle_top: False,
                    BlockType.leaves_right_top: False,
                    }

block_bg = {BlockType.grass: BlockType.bg_dirt,
            BlockType.dirt: BlockType.bg_dirt,
            BlockType.sky: BlockType.sky,
            BlockType.bg_dirt: BlockType.bg_dirt,
            BlockType.stone: BlockType.bg_stone,
            BlockType.bg_stone: BlockType.bg_stone,
            BlockType.tree_bottom: BlockType.sky,
            BlockType.tree_middle: BlockType.sky,
            BlockType.tree_top: BlockType.sky,
            BlockType.leaves_left_bottom: BlockType.sky,
            BlockType.leaves_middle_bottom: BlockType.sky,
            BlockType.leaves_right_bottom: BlockType.sky,
            BlockType.leaves_left_middle: BlockType.sky,
            BlockType.leaves_middle_middle: BlockType.sky,
            BlockType.leaves_right_middle: BlockType.sky,
            BlockType.leaves_left_top: BlockType.sky,
            BlockType.leaves_middle_top: BlockType.sky,
            BlockType.leaves_right_top: BlockType.sky}


class ResourceType:
    grass = 1
    dirt = 1
    stone = 2


resource_images = {ResourceType.grass: pg.image.load("textures/tile_grass.jpg"),
                   ResourceType.dirt: pg.image.load("textures/tile_dirt.png"),
                   ResourceType.stone: pg.image.load("textures/tile_stone.png"), }


class GameStatus:
    in_main_menu = 0
    in_game = 1
    in_pause = 2


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
    jump_right = [
        pg.transform.scale(pg.image.load("animation/character_male_right_jump.png"), (hero_width, hero_height))]
    jump_left = [pg.transform.scale(pg.image.load("animation/character_male_left_jump.png"), (hero_width, hero_height))]
    static = [pg.transform.scale(pg.image.load("animation/character_male_idle.png"), (hero_width, hero_height))]
    break_right = [
        pg.transform.scale(pg.image.load("animation/character_male_right_kick1.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick1.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick2.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick2.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick4.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_right_kick4.png"), (hero_width, hero_height))]
    break_left = [
        pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick2.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick2.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick4.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_left_kick4.png"), (hero_width, hero_height))]
    break_down = [
        pg.transform.scale(pg.image.load("animation/character_male_left_kick1.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick2.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick3.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick4.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick5.png"), (hero_width, hero_height)),
        pg.transform.scale(pg.image.load("animation/character_male_down_kick6.png"), (hero_width, hero_height))]


start_img_off = pg.image.load("menu/button_start_off.png")
start_img_on = pg.image.load("menu/button_start_on.png")
exit_img_on = pg.image.load("menu/button_exit_on.png")
exit_img_off = pg.image.load("menu/button_exit_off.png")
load_save_on = pg.image.load("menu/button_load_save_on.png")
load_save_off = pg.image.load("menu/button_load_save_off.png")
LABaria_pict = pg.image.load("menu/LABaria.png")
back_img_off = pg.image.load("menu/button_back_off.png")
back_img_on = pg.image.load("menu/button_back_on.png")
save_game_img_off = pg.image.load("menu/button_save_game_off.png")
save_game_img_on = pg.image.load("menu/button_save_game_on.png")