import pygame
from constant import *
import os
from sprite import *
from mapgen import Tree

pygame.init()


class Tile(pygame.sprite.Sprite):
    """
    Class for the tiles of map

    Attributes: 
        x (int, arg): x position of tile
        y (int, arg): y position of tile
        game (game, arg): game with object data
        seen (bool): if tile was seen
    """

    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * SPRITE_SIZE
        self.rect.y = y * SPRITE_SIZE
        self.game.all_tile.add(self)
        self.seen = False


class Wall(Tile):
    """
    Class for Wall

    Attributes:
        image_unexplored (surface, arg): image of unexplored wall
        image_explored (surface, arg): image of unexplored wall
        image (surface, arg): current image of wall
        game (game, arg): game with object data
    """

    def __init__(self, game, x, y, image_unexplored=None, image_explored=None):
        self.image_explored = game.game_sprites.seen_wall_image
        self.image_unexplored = game.game_sprites.wall_image
        self.image = self.image_unexplored
        if (image_unexplored):
            self.image_unexplored = image_unexplored
        if (image_explored):
            self.image_explored = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, game, x, y)
        self.game.walls.add(self)


class Floor(Tile):
    """
    Class for Floor

    Attributes:
        image_unexplored (surface, arg): image of unexplored floor
        image_explored (surface, arg): image of unexplored floor
        image (surface, arg): current image of floor
        game (game, arg): game with object data
    """

    def __init__(self, game, x, y, image_unexplored=None, image_explored=None):
        self.image_explored = game.game_sprites.seen_floor_image_1
        self.image_unexplored = game.game_sprites.floor_image_1
        self.image = self.image_unexplored
        if (image_unexplored):
            self.image_unexplored = image_unexplored
        if (image_explored):
            self.image_explored = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, game, x, y)
        # self.game.floors.add(self)


class MapInfo:
    """
    Load map info of map_array into MapInfo

    Attribute:
        tilewidth (int): # of tiles wide
        tileheight (int): # of tiles tall
        width (int): actual width of map
        height (int): actual height of map
    """

    def __init__(self, map_array):
        self.tilewidth = len(map_array[0])
        self.tileheight = len(map_array)
        self.width = self.tilewidth * SPRITE_SIZE
        self.height = self.tileheight * SPRITE_SIZE


def load_map():
    """
    Load data from map.txt and returns map

    Returns:
        map_array (2D array): 2D array loaded with map data from
        with map.txt
    """
    map_data = 'map.txt'
    map_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
    map_array = []
    with open(os.path.join(map_dir, map_data), 'rt') as output:
        for line in output:
            map_array.append(line.strip())
    return map_array


class MapInfo:
    """
    Load map data from map_array

    Args:
        map_array ([[char]char]): 2D array representing map to get
                                        data from

    Attribute:
        tilewidth (int): # of tiles wide
        tileheight (int): # of tiles tall
        width (int): actual width of map
        height (int): actual height of map
    """

    def __init__(self, map_array):
        self.tilewidth = len(map_array[0])
        self.tileheight = len(map_array)
        self.width = self.tilewidth * SPRITE_SIZE
        self.height = self.tileheight * SPRITE_SIZE


def gen_map(game):
    """
    Generates random map and prints resulting map into console. Also draws map to surface
    """
    map_array = [["1" for x in range(0, MAP_WIDTH)] for y in range(0, MAP_HEIGHT)]
    tree = Tree(map_array)
    tree.build_bsp()
    tree.make_room()
    tree.build_path()
    # tree.print_tree()
    tree.print_map()
    game.map_tree = tree
    return map_array


def draw_map(p_map_array, game):

    """
    Draws tiles to background using p_map_array and returns 
    array filled with Tiles

    Args:
        p_map_array ([char[char]]): map to draw as background
        game: (Game): game with all game data
    """
    map_array = []
    for col, tiles in enumerate(p_map_array):
        map_array_row = []
        for row, tile in enumerate(tiles):
            if tile == WALL:
                map_array_row.append(Wall(game, row, col))
            elif tile == FLOOR:
                map_array_row.append(Floor(game, row, col))
            elif tile == PATH:
                map_array_row.append(
                    Floor(game, row, col, game.game_sprites.floor_image_2, game.game_sprites.seen_floor_image_2))
        map_array.append(map_array_row)
    return map_array