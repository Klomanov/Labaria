import pygame
import pygame as pg
import visual
from block import *
from constants import *
from world import *
from hero import *
from physics_process import *


def world_move_general(world, physics_process, hero):
    """Функция, которая осуществляет движение мира с помощью других функций в world_move.py"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        physics_process.world_movement_speed_x = world_move_right()
    elif keys[pygame.K_d]:
        physics_process.world_movement_speed_x = world_move_left()
    else:
        physics_process.world_movement_speed_x = 0
    if keys[pygame.K_SPACE]:
        if check_block(world):
            physics_process.world_movement_speed_y = world_jump()


def main():
    pg.init()
    finished = False
    screen = pg.display.set_mode((width, height))
    drawer = visual.Drawer(screen)
    physic_process = Physic_process(gravconst)
    clock = pg.time.Clock()
    world = init_world()
    hero = Hero()

    while not finished:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
        world_move_general(world, physic_process, hero)
        physic_process.world_move(world)
        physic_process.gravitation(world)
        if physic_process.world_movement_speed_y != 0:
            hero.set_animation(AnimationType.jump)
        else:
            hero.set_animation(AnimationType.static)
        if physic_process.world_movement_speed_x > 0:
            hero.set_animation(AnimationType.left)
        if physic_process.world_movement_speed_x < 0:
            hero.set_animation(AnimationType.right)
        drawer.update_screen(world, hero)


if __name__ == "__main__":
    main()