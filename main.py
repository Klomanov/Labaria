import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *


def main():
    pg.init()
    finished = False
    bottom_down = None  # переменная для движения с зажатой кнопкой
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
            elif event.type == pygame.KEYUP:
                bottom_down = None
        if bottom_down == "a":
            world_move_right(world)
        elif bottom_down == "d":
            world_move_left(world)

        drawer.display_world(world)


if __name__ == "__main__":
    main()
