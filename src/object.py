import os
import pygame
from constant import *

pygame.init()


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
    return image, image.get_rect()





class object(pygame.sprite.Sprite):
    """
    Class for object which represents entity, which is anything that appears
    and acts in the game

    Attributes:
        x (arg, int): Position on x axis
        y (arg, int): Position on y axis
        image (arg, string): Path to image of entity
    """

    def __init__(self, game, x, y, object_id, image, creature=None, ai=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = loadImage(image, -1)
        self.object_id = object_id
        self.x = x
        self.y = y 
        self.rect.topleft = (self.x*SPRITE_SIZE, self.y*SPRITE_SIZE)
        
        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self


    def update(self, dx, dy, game):
        if self.object_id == "player":
            self.creature.move(dx, dy, game)
        if self.ai:
            self.ai.takeTurn(game)



