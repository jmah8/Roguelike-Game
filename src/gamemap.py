import sys
from sprite import *
from map_generator import Tree
from pathfinding import *

pygame.init()


class Tile(pygame.sprite.Sprite):
    """
    Class for the tiles of map

    Attributes: 
        x (int, arg): x position of tile
        y (int, arg): y position of tile
        seen (bool): if tile was seen
        list (arg, list): list to add tile to
    """

    def __init__(self, x, y, list):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect.x = x * SPRITE_SIZE
        self.rect.y = y * SPRITE_SIZE
        self.list = list
        self.list.append(self)
        self.seen = False



class Wall(Tile):
    """
    Class for Wall

    Attributes:
        image_seen (surface, arg): image of explored and seen wall
        image_in_fov (surface, arg): image of wall when in fov
        image (surface, arg): current image of wall
        sprite_dict (game, arg): game with object data
        list (arg, list): list of walls to add self to

    Args:
        image_unexplored (arg, Sprite): sprite of unexplored wall if default is not the
            sprite needed
        image_explored (arg, Sprite): sprite of explored wall if default is not the
            sprite needed
    """

    def __init__(self, sprite_dict, x, y, list, image_unexplored=None, image_explored=None):
        self.image_seen = sprite_dict.seen_wall_image
        self.image_in_fov = sprite_dict.wall_image
        self.image = self.image_in_fov
        if image_unexplored:
            self.image_in_fov = image_unexplored
        if image_explored:
            self.image_seen = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, x, y, list)


class Floor(Tile):
    """
    Class for Floor

    Attributes:
        image_seen (surface, arg): image of explored and seen wall
        image_in_fov (surface, arg): image of wall when in fov
        image (surface, arg): current image of floor
        sprite_dict (game, arg): game with object data
        list (arg, list): list of floor to add self to

    Args:
        image_unexplored (arg, Sprite): sprite of unexplored floor if default is not the
            sprite needed
        image_explored (arg, Sprite): sprite of explored floor if default is not the
            sprite needed
    """

    def __init__(self, sprite_dict, x, y, list, image_unexplored=None, image_explored=None):
        self.image_seen = sprite_dict.seen_floor_image_1
        self.image_in_fov = sprite_dict.floor_image_1
        self.image = self.image_in_fov
        if (image_unexplored):
            self.image_in_fov = image_unexplored
        if (image_explored):
            self.image_seen = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, x, y, list)


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
        tile_width (int): # of tiles wide
        tile_height (int): # of tiles tall
        pixel_width (int): pixel_width of map in pixels
        pixel_height (int): pixel_height of map in pixels
        unseen_tiles (set): set of unseen tiles coord tuple
    """

    def __init__(self, map_array):
        self.tile_width = len(map_array[0])
        self.tile_height = len(map_array)
        self.pixel_width = self.tile_width * SPRITE_SIZE
        self.pixel_height = self.tile_height * SPRITE_SIZE
        self.unseen_tiles = set()

        # if READ_FROM_FILE:
        #     # Holds the map representation (chars)
        #     self.map_array = load_map()
        #
        # # This is for generating random maps
        # else:
        #     # Holds the map representation (chars)
        #     self.map_array = gen_map()
        #
        # # Holds actual tiles
        # self.tile_array = draw_map_menu(self.map_array, self)


        for y in range(self.tile_height):
            for x in range(self.tile_width):
                if not map_array[y][x] == WALL:
                    self.unseen_tiles.add((x, y))


def gen_map(game):
    """
    Generates random map and prints resulting map into console. Also draws map to surface
    """
    map_array = [["1" for x in range(0, MAP_WIDTH)] for y in range(0, MAP_HEIGHT)]
    tree = Tree(map_array)
    tree.build_bsp()
    tree.build_rooms()
    tree.build_path()
    tree.print_map()
    game.map_tree = tree
    return map_array


def draw_map(p_map_array, sprite_dict, wall_list, floor_list):
    """
    Draws tiles to background using p_map_array and returns 
    array filled with Tiles

    Args:
        floor_list (list): list containing floor tiles
        wall_list (list): list containing wall tiles
        p_map_array ([char[char]]): map to draw as background
        sprite_dict: (Game): game with all game data
    """
    map_array = []
    for col, tiles in enumerate(p_map_array):
        map_array_row = []
        for row, tile in enumerate(tiles):
            if tile == WALL:
                map_array_row.append(Wall(sprite_dict, row, col, wall_list))
            elif tile == FLOOR:
                map_array_row.append(Floor(sprite_dict, row, col, floor_list))
            elif tile == PATH:
                map_array_row.append(
                    Floor(sprite_dict, row, col, floor_list, sprite_dict.floor_image_2,
                          sprite_dict.seen_floor_image_2))
        map_array.append(map_array_row)
    return map_array


def find_closest_unseen_tile(game):
    """
    Find closest unseen_tile from player

    Closest tile is by distance, not amount of
    tiles walked to get to it

    Args:
        game (Game): Game with all game data

    Returns:
        p_coord ((int, int)): player's coordinate (start)
        closest_unseen_tile ((int, int)): closest unseen tile (goal)
    """
    closest_unseen_tile = None
    closest_distance = sys.maxsize
    p_coord = (game.player.x, game.player.y)
    # Find the closest (by literal distance, not
    # how many steps it would take) unseen tile
    for tile in game.map_info.unseen_tiles:
        dist = distance(p_coord, tile)
        if closest_distance > dist:
            closest_distance = dist
            closest_unseen_tile = tile
    return p_coord, closest_unseen_tile


# TODO: could optimize this since it is already finding visited and so can
#       return it instead of recalculating it. Results in major performance
#       hit when map is big
def find_closest_unseen_tile_walking_distance(game):
    """
    Find closest unseen_tile from player

    Closest tile is by walking distance, ie how many tile
    would you have to walk. Therefore this takes into account
    walls

    Args:
        game (Game): Game with all game data

    Returns:
        p_coord ((int, int)): player's coordinate (start)
        closest_unseen_tile ((int, int)): closest unseen tile (goal)
    """
    closest_unseen_tile = None
    closest_distance = sys.maxsize
    p_coord = (game.player.x, game.player.y)
    # Find the closest unseen tile
    for tile in game.map_info.unseen_tiles:
        visited = game.graph.bfs(p_coord, tile)
        if visited:
            walking_distance = len(visited)
            if closest_distance > walking_distance:
                closest_distance = walking_distance
                closest_unseen_tile = tile
    return p_coord, closest_unseen_tile
