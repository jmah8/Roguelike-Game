import os
import pygame
import object
import constant

pygame.init()

class tile:
    '''
    Class for the tiles of map

    Attributes: 
        walkable (arg, bool) : True if tile is walkable by objects, false
        otherwise
    '''
    def __init__(self, walkable):
        self.walkable = walkable




def create_map():
    '''
    Returns a map where the outer edges are walls and everything else is a tile.
    '''
    create_map = []
    for x in range (0, (constant.RESOLUTION[0] // constant.SPRITE_SIZE)):
        create_map_row = []
        for y in range (0, (constant.RESOLUTION[1] // constant.SPRITE_SIZE)):
            if ((y == 0 or y == (constant.RESOLUTION[1] // constant.SPRITE_SIZE) - 1)
            or (x == 0 or x == (constant.RESOLUTION[0] // constant.SPRITE_SIZE) - 1)):
                create_map_row.append(tile(False))
            else:
                create_map_row.append(tile(True))
        create_map.append(create_map_row)
    return create_map
