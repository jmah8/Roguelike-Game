import pygame
import constant
import object

pygame.init()

class tile:
    """
    Class for the tiles of map

    Attributes: 
        walkable (arg, bool) : True if tile is walkable by objects, false
        otherwise
    """
    def __init__(self, walkable):
        self.walkable = walkable




def create_map():
    """
    Returns a map where the outer edges are walls and everything else is a tile.
    """
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



# TODO: change path for images to constant when right picture is found
def draw_map(map_to_draw, surface):
    """
    Draws map and makes walkable = True to floor and walkable = False wall

    Loops through every tile in map and draws it in correct position

    Arg:
        map_to_draw (array): map to draw as background
    """
    for x in range(0, (constant.RESOLUTION[0] // constant.SPRITE_SIZE)):
        for y in range(0, (constant.RESOLUTION[1] // constant.SPRITE_SIZE)):
            if map_to_draw[x][y].walkable == True:
                floor = object.loadImage('16x16/tiles/floor/floor_1.png')
                surface.blit(
                    floor[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))
            else:
                wall = object.loadImage('16x16/tiles/wall/wall_1.png')
                surface.blit(
                    wall[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))