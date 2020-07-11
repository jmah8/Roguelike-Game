import pygame
from constant import *
import object
import os
from sprite import *

pygame.init()

class tile(pygame.sprite.Sprite):
    """
    Class for the tiles of map

    Attributes: 
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
        self.game.all_sprites.add(self)

class wall(tile):
    def __init__(self, game, x, y):
        self.image = game.game_sprites.wall_image
        self.rect = self.image.get_rect()
        tile.__init__(self, game, x, y)
        self.game.walls.add(self)

class floor(tile):
    def __init__(self, game, x, y):
        self.image = game.game_sprites.floor_image
        self.rect = self.image.get_rect()
        tile.__init__(self, game, x, y)
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


# TODO: change path for images to constant when right picture is found
def draw_map(map_to_draw, game):
    """
    Draws map and makes walkable = True to floor and walkable = False wall

    Loops through every tile in map and draws it in correct position

    Arg:
        map_to_draw (arg, array): map to draw as background
        game (arg, game): game with data
    """
    map_array = []
    fov = []
    for row, tiles in enumerate(map_to_draw):
        map_array_row = []
        fov_row = []
        for col, tile in enumerate(tiles):
            if tile == '1':
                map_array_row.append(wall(game, col, row))
            if tile == '.':
                map_array_row.append(floor(game, col, row))
            fov_row.append(0)
        map_array.append(map_array_row)
        fov.append(fov_row)
    return map_array, fov 
  

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
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

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
        x = -player.rect.x + int(MAP_WIDTH / 2)
        y = -player.rect.y + int(MAP_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - MAP_WIDTH), x)
        y = max(-(self.height - MAP_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)




def ray_casting(game, map_array, fov):
    for a in range(0, RAYS + 1, STEP):
        ax = sintable[a]
        ay = costable[a]

        x = game.player.x
        y = game.player.y

        for b in range(RAD):
            x += ax
            y += ay

            if x < 0 or y < 0 or x > MAP_WIDTH or y > MAP_HEIGHT:
                break
                
            fov[int(round(y))][int(round(x))] = 1

            if isinstance(game.map_array[int(round(y))][int(round(x))], wall):
                break


def draw_seen(game, map_array, fov):
    for y in range(0, game.map_tiles.tileheight):
        for x in range(0, game.map_tiles.tilewidth):
            if (x, y) == (game.player.x, game.player.y):
                map_array[y][x].image = game.game_sprites.seen_floor
            elif fov[y][x] == 1:
                if isinstance(map_array[y][x], floor):
                    map_array[y][x].image = game.game_sprites.seen_floor
                else:
                    map_array[y][x].image = game.game_sprites.wall_image
            else:
                map_array[y][x].image = game.game_sprites.unseen_floor