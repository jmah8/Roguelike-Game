import os
import pygame
from loadAsset import loadImage
import constant

pygame.init()

class tile:
    def __init__(self, walkable):
        self.walkable = walkable


def create_map():
    create_map = [[ tile(True) for y in range(0, (constant.RESOLUTION[1] // constant.SPRITE_SIZE))] for x in range(0, (constant.RESOLUTION[0] // constant.SPRITE_SIZE))]

    create_map[1][2].walkable = False
    create_map[3][4].walkable = False

    return create_map
