import pygame
from constant import *
import object
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

class TileMap:
    """
    Load map data for filename.txt

    Arg:
        filename (arg, string): name of file to read from 

    Attribute:
        tilewidth (int): # of tiles wide
        tileheight (int): # of tiles tall
        width (int): actual width of map
        height (int): actual height of map
    """
    def __init__(self, filename):
        map_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
        self.data = []
        with open(os.path.join(map_dir, filename), 'rt') as output:
            for line in output:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * SPRITE_SIZE
        self.height = self.tileheight * SPRITE_SIZE

        

def load_data():
    """
    Load data from map.txt and returns TileMap instance
    """
    map_data = TileMap('map.txt')
    return map_data



def draw_map(map_to_draw, game):
    """
    Draws map and makes walkable = True to floor and walkable = False wall

    Loops through every tile in map and draws it in correct position

    Arg:
        map_to_draw (arg, array): map to draw as background
        game (arg, game): game with data
    """
    map_array = []
    # fov = []
    for row, tiles in enumerate(map_to_draw):
        map_array_row = []
        # fov_row = []
        for col, tile in enumerate(tiles):
            if tile == WALL:
                map_array_row.append(Wall(game, col, row))
            if tile == FLOOR:
                map_array_row.append(Floor(game, col, row))
            # fov_row.append(0)
        map_array.append(map_array_row)
        # fov.append(fov_row)
    return map_array 


class MapInfo:
    """
    Load map data from map_array

    Arg:
        map_array ([[char]char], arg): 2D array representing map to get 
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
    map_array = [["1" for x in range (0, MAP_WIDTH)] for y in range (0, MAP_HEIGHT)]
    tree = Tree(map_array)
    tree.build_bsp()
    tree.make_room()
    tree.build_path()
    tree.print_tree()
    tree.print_map()
    return draw_tiles(map_array, game)


def draw_tiles(p_map_array, game):
    """
    Draws tiles to background using p_map_array and returns 
    array filled with Tiles

    Arg:
        p_map_array ([char[char]], arg): map to draw as background
        game: (Game, arg): game with all game data
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
                map_array_row.append(Floor(game, row, col, game.game_sprites.floor_image_2, game.game_sprites.seen_floor_image_2))
        map_array.append(map_array_row)
    return map_array


class Camera:
    """
    Camera that "follows" player around

    Camera is actually the whole map that gets offset whenever
    player moves and it offsets everything else relative to
    the camera's offset

    Arg:
        width (arg, int): width of whole map
        height (arg, int): height of whole map
        camera (rect): rect of whole map
    """
    def __init__(self, width, height, camera_width=CAMERA_WIDTH, camera_height=CAMERA_HEIGHT):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height

    def apply(self, entity):
        """
        Apply camera offset to entity 

        Arg:
            entity (arg, object): object to apply offset to
        """
        return entity.rect.move(self.camera.topleft)
    
    def update(self, player):
        """
        Update the camera based on player position

        Arg:
            player (arg, object): player to follow
        """
        x = -player.rect.x + int(self.camera_width / 2)
        y = -player.rect.y + int(self.camera_height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - self.camera_width), x)
        y = max(-(self.height - self.camera_height), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)



def new_fov(game):
    new_fov = [[0 for x in range (0, game.map_tiles.tilewidth)] for y in range (game.map_tiles.tileheight)]
    return new_fov


def ray_casting(game, map_array, fov):
    for a in range(0, RAYS + 1, STEP):
        ax = sintable[a]
        ay = costable[a]

        x = game.player.x
        y = game.player.y

        for b in range(KNIGHT_FOV):
            x += ax
            y += ay

            if x < 0 or y < 0 or x > game.map_tiles.tilewidth - 1 or y > game.map_tiles.tileheight - 1:
                break
                
            fov[int(round(y))][int(round(x))] = 1

            if isinstance(game.map_array[int(round(y))][int(round(x))], Wall):
                break
    
    fov[game.player.y][game.player.x] = 1


def draw_seen(game, map_array, fov):
    for y in range(0, game.map_tiles.tileheight):
        for x in range(0, game.map_tiles.tilewidth):
            tile = map_array[y][x]
            if (x, y) == (game.player.x, game.player.y):
                tile.image = tile.image_unexplored
            elif fov[y][x] == 1:
                if isinstance(tile, Floor):
                    tile.image = tile.image_unexplored
                else:
                    tile.image = tile.image_unexplored
                tile.seen = True
            else:
                tile = map_array[y][x]
                if (not tile.seen):
                    tile.image = game.game_sprites.unseen_tile
                else:
                    tile.image = tile.image_explored


def check_if_in_fov(game, obj):
    """
    Checks to see if sprite is in player FOV

    Arg:
        sprite (arg, sprite): sprite to check
    """
    x = obj.x
    y = obj.y
    if (game.fov[y][x] == 1):
        return True