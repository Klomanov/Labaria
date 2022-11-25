import pygame
import pygame as pg
import visual
from block import *
from constants import *
from  world_move import *


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
    bottom_down = None  #переменная для движения с зажатой кнопкой
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    clock = pg.time.Clock()
    world = init_world()

    while not finished:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    bottom_down = "a"
                    world_move_right(world)
                elif event.key == pygame.K_d:
                    world_move_left(world)
                    bottom_down = "d"
            elif bottom_down == "a":
                world_move_right(world)
            elif bottom_down == "d":
                world_move_left(world)
            elif event.type == pygame.KEYUP:
                bottom_down = None
        drawer.display_world(world)


if __name__ == "__main__":
    main()
