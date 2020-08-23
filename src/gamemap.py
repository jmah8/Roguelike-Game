import sys
import config
from sprite import *
from map_generator import Tree
from pathfinding import *

pygame.init()

class Tile:

    def __init__(self, x, y, type):
        """
        Class that holds information about tile

        Args:
            x (int): x coord of tile
            y (int): y coord of tile
            type (string): the type of tile it is as a char
        """
        self.x = x
        self.y = y
        self.type = type
        self.seeing = False
        self.seen = False

    @property
    def image(self):
        """
        Returns:
            Returns image tile should have
        """
        if self.seen and self.seeing:
            return config.SPRITE.tile_dict[self.type]["seeing"]
        elif self.seen:
            return config.SPRITE.tile_dict[self.type]["seen"]
        else:
            return config.SPRITE.tile_dict["unseen"]

    @property
    def rect(self):
        """
        Returns tile's rect position, ie where the tile is on the screen,
        which is different then self.x, self.y which is the position of tile
        in game

        Returns:
            Tile's rect position
        """
        return self.x * SPRITE_SIZE, self.y * SPRITE_SIZE

    @property
    def size(self):
        """
        Returns:
            Tile's sprite size, which is usually SPRITE_SIZE
        """
        return SPRITE_SIZE, SPRITE_SIZE

class MapInfo:
    """
    Load map data from map_array or generates map. Holds map arrays

    Args:
        game (Game): game with all game data

    Attribute:
        map_array (2D array): array with map representation
        self.map_tree (Tree): BSP tree of map
        tile_array (2D array): array with tiles
        tile_width (int): # of tiles wide
        tile_height (int): # of tiles tall
        pixel_width (int): pixel_width of map in pixels
        pixel_height (int): pixel_height of map in pixels
        unseen_tiles (set): set of unseen tiles coord tuple
    """

    def __init__(self):

        if READ_FROM_FILE:
            # Holds the map representation (chars)
            map_array = load_map()
            self.map_tree = None

        # This is for generating random maps
        else:
            # Holds the map representation (chars)
            map_array = [["1" for x in range(0, MAP_WIDTH)] for y in range(0, MAP_HEIGHT)]
            self.map_tree = gen_map(map_array)

        # Holds actual tiles
        self.tile_array = make_tile_array(map_array)

        self.tile_width = len(self.tile_array[0])
        self.tile_height = len(self.tile_array)
        self.pixel_width = self.tile_width * SPRITE_SIZE
        self.pixel_height = self.tile_height * SPRITE_SIZE
        self.unseen_tiles = set()

        for y in range(self.tile_height):
            for x in range(self.tile_width):
                if not self.tile_array[y][x].type == WALL:
                    self.unseen_tiles.add((x, y))


def make_tile_array(map_array):
    """
    Draws tiles to background using p_map_array and returns
    array filled with Tiles

    Args:
        map_array ([char[char]]): map to draw as background
        tile_dict (dictionary): dictionary containing all tile sprites

    Returns:
        tile_array (2D array): array with tiles
    """
    tile_array = []
    for col, tiles in enumerate(map_array):
        tile_array_row = []
        for row, tile in enumerate(tiles):
            tile_array_row.append(Tile(row, col, tile))
        tile_array.append(tile_array_row)
    return tile_array


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


def gen_map(map_array):
    """
    Generates random map and prints resulting map into console. Also draws map to surface

    Args:
        map_array (2D array): array with map representation

    Returns:
        tree (Tree): BSP tree of map
    """
    tree = Tree(map_array)
    tree.build_bsp()
    tree.build_rooms()
    tree.build_path()
    tree.print_map()
    tree.place_downstair()
    print("")
    return tree

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
    p_coord = (config.PLAYER.x, config.PLAYER.y)
    # Find the closest (by literal distance, not
    # how many steps it would take) unseen tile
    for tile in config.MAP_INFO.unseen_tiles:
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
    p_coord = (config.PLAYER.x, config.PLAYER.y)
    # Find the closest unseen tile
    for tile in config.MAP_INFO.unseen_tiles:
        visited = config.PATHFINDING.bfs(p_coord, tile)
        if visited:
            walking_distance = len(visited)
            if closest_distance > walking_distance:
                closest_distance = walking_distance
                closest_unseen_tile = tile
    return p_coord, closest_unseen_tile
