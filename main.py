import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *


def main():
    pg.init()
    finished = False
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    clock = pg.time.Clock()
    world = init_world()
    hero = Hero()

    while not finished:

        clock.tick(60)
        world_move_general(world)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            world_move_right(world)
            hero.set_animation(AnimationType.left)
        elif keys[pygame.K_d]:
            world_move_left(world)
            hero.set_animation(AnimationType.right)
        elif jump:
            hero.set_animation(AnimationType.jump)
        else:
            hero.set_animation(AnimationType.static)

        drawer.update_screen(world, hero)


if __name__ == "__main__":
    main()