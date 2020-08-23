import sys
from sprite import *
from map_generator import Tree
from pathfinding import *

pygame.init()

class TileTest:

    def __init__(self, x, y, sprite_key, type):
        self.x = x
        self.y = y
        self.sprite_key = sprite_key
        self.type = type


class Tile(pygame.sprite.Sprite):
    """
    Class for the tiles of map

    Attributes: 
        x (int, arg): x position of tile
        y (int, arg): y position of tile
        seen (bool): if tile was seen
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.rect.x = x * SPRITE_SIZE
        self.rect.y = y * SPRITE_SIZE
        self.seen = False



class Wall(Tile):
    """
    Class for Wall

    Attributes:
        image_seen (surface, arg): image of explored and seen wall
        image_in_fov (surface, arg): image of wall when in fov
        image (surface, arg): current image of wall
        sprite_dict (game, arg): game with object data

    Args:
        image_unexplored (arg, Sprite): sprite of unexplored wall if default is not the
            sprite needed
        image_explored (arg, Sprite): sprite of explored wall if default is not the
            sprite needed
    """

    def __init__(self, sprite_dict, x, y, image_unexplored=None, image_explored=None):
        self.image_seen = sprite_dict.seen_wall_image
        self.image_in_fov = sprite_dict.wall_image
        self.image = self.image_in_fov
        if image_unexplored:
            self.image_in_fov = image_unexplored
        if image_explored:
            self.image_seen = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, x, y)


class Floor(Tile):
    """
    Class for Floor

    Attributes:
        image_seen (surface, arg): image of explored and seen wall
        image_in_fov (surface, arg): image of wall when in fov
        image (surface, arg): current image of floor
        sprite_dict (game, arg): game with object data

    Args:
        image_unexplored (arg, Sprite): sprite of unexplored floor if default is not the
            sprite needed
        image_explored (arg, Sprite): sprite of explored floor if default is not the
            sprite needed
    """

    def __init__(self, sprite_dict, x, y, image_unexplored=None, image_explored=None):
        self.image_seen = sprite_dict.seen_floor_image_1
        self.image_in_fov = sprite_dict.floor_image_1
        self.image = self.image_in_fov
        if (image_unexplored):
            self.image_in_fov = image_unexplored
        if (image_explored):
            self.image_seen = image_explored
        self.rect = self.image.get_rect()
        Tile.__init__(self, x, y)


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

    def __init__(self, game):

        if READ_FROM_FILE:
            # Holds the map representation (chars)
            self.map_array = load_map()
            self.map_tree = None

        # This is for generating random maps
        else:
            # Holds the map representation (chars)
            self.map_array = [["1" for x in range(0, MAP_WIDTH)] for y in range(0, MAP_HEIGHT)]
            self.map_tree = gen_map(self.map_array)

        # Holds actual tiles
        self.tile_array = draw_map(self.map_array, game.game_sprites)

        self.tile_width = len(self.map_array[0])
        self.tile_height = len(self.map_array)
        self.pixel_width = self.tile_width * SPRITE_SIZE
        self.pixel_height = self.tile_height * SPRITE_SIZE
        self.unseen_tiles = set()

        for y in range(self.tile_height):
            for x in range(self.tile_width):
                if not self.map_array[y][x] == WALL:
                    self.unseen_tiles.add((x, y))


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


def draw_map(map_array, sprite_dict):
    """
    Draws tiles to background using p_map_array and returns 
    array filled with Tiles

    Args:
        map_array ([char[char]]): map to draw as background
        sprite_dict: (GameSprites): dict with all sprites

    Returns:
        tile_array (2D array): array with tiles
    """
    tile_array = []
    for col, tiles in enumerate(map_array):
        tile_array_row = []
        for row, tile in enumerate(tiles):
            if tile == WALL:
                tile_array_row.append(Wall(sprite_dict, row, col))
            elif tile == FLOOR:
                tile_array_row.append(Floor(sprite_dict, row, col))
            elif tile == PATH:
                tile_array_row.append(
                    Floor(sprite_dict, row, col, sprite_dict.floor_image_2, sprite_dict.seen_floor_image_2))
            elif tile == DOWNSTAIR:
                tile_array_row.append(
                    Floor(sprite_dict, row, col, sprite_dict.downstair, sprite_dict.seen_downstair))
            elif tile == UPSTAIR:
                tile_array_row.append(
                    Floor(sprite_dict, row, col, sprite_dict.upstair, sprite_dict.seen_upstair))
        tile_array.append(tile_array_row)
    return tile_array


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
