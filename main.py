import pygame as pg
import visual
from block import *
from constants import *


def init_world(width, height):
    world = []
    start_point_x = 100
    start_point_y = 100
    for y in range(height):
        world.append([])
        for x in range(width):
            world[y].append(Block(start_point_x + x*block_size, start_point_y + y*block_size, BlockType.dirt))

    return world


def main():

    pg.init()
    finished = False

    width = 1200
    height = 800
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    clock = pg.time.Clock()
    world = init_world(10, 1)

    while not finished:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        drawer.update(world, None)


if __name__ == "__main__":
    main()
