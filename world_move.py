import pygame as pg


def world_move_left(world):
    for type_block in world:
        for block in type_block:
            block.x -= 1


def world_move_right(world):
    for type_block in world:
        for block in type_block:
            block.x += 1

def world_move_down(world):
    for block in world:
        block.y -= 1

def world_move_up(world):
    for block in world:
        block.y += 1