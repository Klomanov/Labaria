import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *


def init_world():
    """
    Инициализирует мир в три этапа. Небо, трава, земля
    :return: массив мира
    """
    world = []
    for y in range(sky_level):
        world.append([])
        for x in range(world_size_x):
            world[y].append(Block(x*block_size, block_size*y, BlockType.sky))

    world.append([])
    for x in range(world_size_x):
        world[0].append(Block(x*block_size, block_size*sky_level, BlockType.grass))

    for y in range(sky_level+1, world_size_y):
        world.append([])
        for x in range(world_size_x):
            world[y].append(Block(block_size*x, block_size*y, BlockType.dirt))

    return world


def main():
    pg.init()
    finished = False
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    clock = pg.time.Clock()
    world = init_world()
    hero = Hero(screen)

    while not finished:
        clock.tick(60)
        world_move_general(world)
        drawer.display_world(world)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            world_move_right(world)
            hero.draw_hero('a', sky_level)
        elif keys[pygame.K_d]:
            world_move_left(world)
            hero.draw_hero('d', sky_level)
        elif jump:
            hero.draw_hero('j', sky_level)
        else:
            hero.static(sky_level)

        pg.display.update()


if __name__ == "__main__":
    main()