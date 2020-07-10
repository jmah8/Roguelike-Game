import pygame
from constant import *
import object
import os

pygame.init()


class tile(pygame.sprite.Sprite):
    """
    Class for the tiles of map

    Attributes: 
        walkable (arg, bool) : True if tile is walkable by objects, false
        otherwise
        x (arg, int): x position of tile
        y (arg, int): y position of tile
        game (arg, game): game with object data
    """

    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * SPRITE_SIZE
        self.rect.y = y * SPRITE_SIZE


class wall(tile):
    def __init__(self, game, x, y):
        self.image, self.rect = object.loadImage(WALL_1)
        tile.__init__(self, game, x, y)
        self.game.walls.add(self)


class floor(tile):
    def __init__(self, game, x, y):
        self.image, self.rect = object.loadImage(FLOOR_1)
        tile.__init__(self, game, x, y)
        self.game.floors.add(self)


def load_data():
    map_dir = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'resource')
    map_tile = []
    with open(os.path.join(map_dir, 'map.txt'), 'rt') as output:
        for line in output:
            map_tile.append(line.strip())
    return map_tile


# TODO: change path for images to constant when right picture is found
def draw_map(map_to_draw, game):
    """
    Draws map and makes walkable = True to floor and walkable = False wall

    Loops through every tile in map and draws it in correct position

    Arg:
        map_to_draw (arg, array): map to draw as background
        game (arg, game): game with data
    """
    for row, tiles in enumerate(map_to_draw):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall(game, col, row)
            if tile == '.':
                floor(game, col, row)


def check_map_for_creature(x, y, exclude_object):
    """
    if excluded_object != None, 
    check map to see if creature at (x,y) is a not excluded_object
    else check map to see if any creature at (x,y)
    """
    if exclude_object:
        target = None
        for object in game_objects:
            if (object is not exclude_object and object.x == x and object.y == y and object.creature):
                target = object
                return target

    else:
        target = None
        for object in game_objects:
            if (object.x == x and object.y == y and object.creature):
                target = object
                return target


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(MAP_WIDTH / 2)
        y = -target.rect.centery + int(MAP_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - MAP_WIDTH), x)
        y = max(-(self.height - MAP_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
