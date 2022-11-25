import pygame as pg
"""Осуществляет движение мира"""


def world_move_left(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for type_block in world:
        for block in type_block:
            block.x -= 1


def world_move_right(world):
    """Движение мира влево, использовать при движении игрока вправо"""
    for type_block in world:
        for block in type_block:
            block.x += 1


def world_move_down(world):
    """Пока что ненужная функция"""
    for type_block in world:
        for block in type_block:
            block.y += 1


def world_move_up(world):
    """Пока что ненужная функция"""
    for type_block in world:
        for block in type_block:
            block.y -= 1