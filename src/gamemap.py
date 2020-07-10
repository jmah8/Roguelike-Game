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
        self.game.all_sprites.add(self)

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

class TileMap:
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
    for row, tiles in enumerate(map_to_draw):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall(game, col, row)
            if tile == '.':
                floor(game, col, row)


            

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        print("w:" + str(width) + " " + "h:" + str(height))

    def apply(self, entity):
        # print(self.camera.topleft)
        return entity.rect.move(self.camera.topleft)
    
    def update(self, player):
        x = -player.rect.x + int(MAP_WIDTH / 2)
        y = -player.rect.y + int(MAP_HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - MAP_WIDTH), x)
        y = max(-(self.height - MAP_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)