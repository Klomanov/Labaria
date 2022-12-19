import pygame


class PickledBlock:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type


class PickledWorld:
    def __init__(self, map):
        self.pickled_map = []
        for i in range(len(map)):
            self.pickled_map.append([])
            for j in range(len(map[i])):
                self.pickled_map[i].append([])
                for k in range(len(map[i][j])):
                    pickled_block = PickledBlock(map[i][j][k].x, map[i][j][k].y,
                                                 map[i][j][k].type)
                    self.pickled_map[i][j].append(pickled_block)


class PickledInventory:
    def __init__(self, resources):
        self.resources = {}
        for name, resource in resources.items():
            self.resources[name] = [name, resource.amount]


