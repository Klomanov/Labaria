import pygame
"""Осуществляет движение мира"""

world_movement_speed_y = 0 #переменная, которая отвечает за скорость вертикального движения мира
jump = False #находится персонаж в прыжке или нет


def world_move_left(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for row in world:
        for block in row:
            block.x -= 1


def world_move_right(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for row in world:
        for block in row:
            block.x += 1


def world_jump(world):
    """Функция, которая осуществляет прыжок"""
    global world_movement_speed_y, jump
    if world_movement_speed_y == 0 and jump == False:
        world_movement_speed_y = 6.5
    elif world_movement_speed_y > -7:
        for row in world:
            for block in row:
                block.y += world_movement_speed_y
        world_movement_speed_y -= 0.5
    elif world_movement_speed_y == -7:
        world_movement_speed_y = 0
        jump = False


def world_move_general(world):
    """Функция, которая осуществляет движение мира с помощью других функций в world_move.py"""
    global jump
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        world_move_right(world)
    if keys[pygame.K_d]:
        world_move_left(world)
    if keys[pygame.K_SPACE] and jump == False:
        world_jump(world)
        jump = True
    elif jump:
        world_jump(world)


def world_move_down(world):
    """Пока что ненужная функция"""
    for strings in world:
        for block in strings:
            block.y += 1


def world_move_up(world):
    """Пока что ненужная функция"""
    for strings in world:
        for block in strings:
            block.y -= 1