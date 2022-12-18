import pygame as pg

block_size = 30
screen_height = 800
screen_width = 1200
font_size = 24

g = 1  # ускорение свободного падения

chunk_num = 4  # Нельзя менять!!!
chunk_size: int = 120
world_size_x = chunk_size * chunk_num
world_size_y = screen_height // block_size + 80  # Высота карты мира
sky_level = 30  # s Уровень неба
bedrock_level = world_size_y - 15  # Уровень коренной породы

caves_frequency = 1  # Частота пещер
tree_frequency = 1  # Частота деревьев
decorations_frequency = 1  # Частота декораций

hero_spawn_x = screen_width // 2  # Место спавна героя
hero_spawn_y = screen_height // 2
hero_width = 1.75 * block_size  # Геометрические размеры героя
hero_height = 1.95 * block_size
hero_speed = 4  # Кинематические свойства героя (в целых числах все нужно указывать)
hero_jump_power = 20
hero_dig_range = 3 * block_size

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
    bedrock = 18
    dec_grass1 = 19
    dec_grass2 = 20
    dec_grass3 = 21
    dec_grass4 = 22
    dec_mushroom_brown = 23
    dec_mushroom_red = 24
    dec_rock = 25
    dec_rock_moss = 26
    log = 27


block_images = {BlockType.grass: pg.image.load("textures/tile_grass.jpg"),
                BlockType.dirt: pg.image.load("textures/tile_dirt.png"),
                BlockType.sky: pg.image.load("textures/tile_sky.png"),
                BlockType.log: pg.image.load("textures/wood_inventory.png"),
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
                BlockType.leaves_right_top: pg.image.load("textures/tree/tile_leaves_right_top.png"),
                BlockType.bedrock: pg.image.load("textures/tile_bedrock.png"),
                BlockType.dec_grass1: pg.image.load("textures/decorations/tile_grass1.png"),
                BlockType.dec_grass2: pg.image.load("textures/decorations/tile_grass2.png"),
                BlockType.dec_grass3: pg.image.load("textures/decorations/tile_grass3.png"),
                BlockType.dec_grass4: pg.image.load("textures/decorations/tile_grass4.png"),
                BlockType.dec_mushroom_brown: pg.image.load("textures/decorations/tile_mushroom_brown.png"),
                BlockType.dec_mushroom_red: pg.image.load("textures/decorations/tile_mushroom_red.png"),
                BlockType.dec_rock: pg.image.load("textures/decorations/tile_rock.png"),
                BlockType.dec_rock_moss: pg.image.load("textures/decorations/tile_rock_moss.png"), }

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
                       BlockType.bedrock: None,
                       BlockType.dec_grass1: 0.2,
                       BlockType.dec_grass2: 0.2,
                       BlockType.dec_grass3: 0.2,
                       BlockType.dec_grass4: 0.2,
                       BlockType.dec_mushroom_brown: 0.2,
                       BlockType.dec_mushroom_red: 0.2,
                       BlockType.dec_rock: 0.2,
                       BlockType.dec_rock_moss: 0.2,
                       BlockType.log: 0.75,
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
                    BlockType.bedrock: True,
                    BlockType.dec_grass1: False,
                    BlockType.dec_grass2: False,
                    BlockType.dec_grass3: False,
                    BlockType.dec_grass4: False,
                    BlockType.dec_mushroom_brown: False,
                    BlockType.dec_mushroom_red: False,
                    BlockType.dec_rock: False,
                    BlockType.dec_rock_moss: False,
                    BlockType.log: True
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
            BlockType.leaves_right_top: BlockType.sky,
            BlockType.bedrock: BlockType.bg_stone,
            BlockType.dec_grass1: BlockType.sky,
            BlockType.dec_grass2: BlockType.sky,
            BlockType.dec_grass3: BlockType.sky,
            BlockType.dec_grass4: BlockType.sky,
            BlockType.dec_mushroom_brown: BlockType.sky,
            BlockType.dec_mushroom_red: BlockType.sky,
            BlockType.dec_rock: BlockType.bg_stone,
            BlockType.dec_rock_moss: BlockType.bg_stone,
            BlockType.log: BlockType.sky,
            }


class ResourceType:
    grass = 0
    dirt = 1
    stone = 2
    mushroom_red = 4
    mushroom_brown = 5
    rock = 6
    rock_moss = 7
    log = 8


# Это массив соответствия ресурса, который выпадает, когда ломаешь блока
block_resource = {BlockType.grass: ResourceType.dirt,
                  BlockType.dirt: ResourceType.dirt,
                  BlockType.stone: ResourceType.stone,
                  BlockType.tree_bottom: ResourceType.log,
                  BlockType.tree_middle: ResourceType.log,
                  BlockType.tree_top: ResourceType.log,
                  BlockType.log: ResourceType.log}

# Это массив соответствия блоку, когда ставишь ресурс
resource_block = {ResourceType.dirt: BlockType.dirt,
                  ResourceType.stone: BlockType.stone,
                  ResourceType.log: BlockType.log}

resource = [ResourceType.grass, ResourceType.dirt,
            ResourceType.stone, ResourceType.log,
            ResourceType.mushroom_red, ResourceType.mushroom_brown,
            ResourceType.rock, ResourceType.rock_moss]

resource_images = {ResourceType.grass: pg.image.load("textures/grass_inventory.png"),
                   ResourceType.dirt: pg.image.load("textures/dirt_inventory.png"),
                   ResourceType.stone: pg.image.load("textures/stone_inventory.png"),
                   ResourceType.log: pg.image.load("textures/wood_inventory1.png"),
                   ResourceType.mushroom_red: pg.image.load("textures/decorations/tile_mushroom_red.png"),
                   ResourceType.mushroom_brown: pg.image.load("textures/decorations/tile_mushroom_brown.png"),
                   ResourceType.rock: pg.image.load("textures/decorations/tile_rock.png"),
                   ResourceType.rock_moss: pg.image.load("textures/decorations/tile_rock_moss.png")}

keys = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7]

cross = pg.image.load("menu/cross.png")

resource_keys = {ResourceType.grass: pg.K_0,
                 ResourceType.dirt: pg.K_1,
                 ResourceType.stone: pg.K_2,
                 ResourceType.log: pg.K_3,
                 ResourceType.mushroom_red: pg.K_4,
                 ResourceType.mushroom_brown: pg.K_5,
                 ResourceType.rock: pg.K_6,
                 ResourceType.rock_moss: pg.K_7}

resource_surnames = {ResourceType.grass: "GRASS",
                     ResourceType.dirt: "DIRT",
                     ResourceType.stone: "STONE",
                     ResourceType.log: "LOG",
                     ResourceType.mushroom_red: "RED MUSHROOM",
                     ResourceType.mushroom_brown: "BROWN MUSHROOM",
                     ResourceType.rock: "ROCK",
                     ResourceType.rock_moss: "ROCK MOSS"}


class GameStatus:
    in_main_menu = 0
    in_game = 1
    in_pause = 2
    in_saves = 3
    in_enter_save = 4


plus = pg.image.load("menu/plus.png")


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


LABaria_pict = pg.image.load("menu/LABaria.png")
button_img_off = pg.image.load("menu/button_off.png")
button_img_on = pg.image.load("menu/button_on.png")
enter_row_img = pg.image.load("menu/enter_row.png")
