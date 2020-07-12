import pygame
from constant import *
import os

def loadImage(name, colorkey=None):
    """
    Load and convert image to surface and returns image and the image rect
    and makes color at colorkey transparent
    Arg:
        name (arg, string) : Pathname of image to convert
        colorkey (arg, (int, int)) : Position of color to be transparent
    """
    dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
    pathname = os.path.join(dirname, name)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(name)
    # convert_alpha() is also an option
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

def seen_sprite(image):
    """
    Converts an image, to a seen image

    Arg:
        image (arg, sprite): image to convert to seen image
    """
    seen_image = image.copy()
    seen_image = image.copy()
    seen_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
    return seen_image



class GameSprites():
    """
    Class that holds all the sprite images
    """
    def __init__(self):
        self.wall_image = loadImage(WALL_1)
        self.floor_image = loadImage(FLOOR_1)
        self.player_image = loadImage(PLAYER)
        self.slime_image = loadImage(SLIME)
        # self.floor_image.fill(GREY, special_flags=pygame.BLEND_RGB_MULT)
        self.unseen_tile = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.unseen_tile.fill(BLACK)
        self.seen_tile = loadImage(SPIKE)
    
