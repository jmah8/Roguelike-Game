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