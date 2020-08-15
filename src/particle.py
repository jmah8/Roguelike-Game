import pygame
import pygame.freetype
from constant import *
import draw

pygame.init()
dirname = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')
font_path_name = os.path.join(dirname, 'fonts/FFF_Tusj.ttf')
myfont = pygame.freetype.Font(font_path_name, 20)


class Particle(pygame.sprite.Sprite):
    """
    Class that represents a particle

    Attributes:
        x (arg, int): x position of particle
        y (arg, int): y position of particle
        group (arg, Group): group particle belongs to
    """

    # TODO: add check for when actual map is smaller than RESOLUTION,
    #       so x and y aren't in sync just like the mouse cursor
    def __init__(self, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.group = group


# class MagicParticle(Particle):
#
#     def __init__(self, x, y, group, image, list):
#         Particle.__init__(self, x, y, group)
#         self.image = image
#         self.rect =


class DamageNumParticle(Particle):
    """
    Class that represents damage number above creature

    Attributes:
        x (arg, int): x position of particle
        y (arg, int): y position of particle
        v_x (int): x velocity of particle
        v_y (int): y velocity of particle
        max_x (int): max x position of particle (after which it disappears)
        max_y (int): max y position of particle (after which it disappears)
        group (arg, Group): group particle belongs to
    """
    def __init__(self, x, y, damage, group):
        Particle.__init__(self, x, y, group)
        self.x += 0.5
        self.v_x = 2 / SPRITE_SIZE
        self.v_y = -5 / SPRITE_SIZE
        self.max_x = self.x + SPRITE_SIZE
        self.max_y = self.y
        self.image, self.rect = myfont.render(str(damage), RED)
        self.rect.topleft = (self.x * SPRITE_SIZE, self.y * SPRITE_SIZE)

    def update(self):
        self.x += self.v_x
        self.y += self.v_y
        self.v_y += 0.25 / SPRITE_SIZE
        self.rect.topleft = (self.x * SPRITE_SIZE, self.y * SPRITE_SIZE)
        if self.y >= self.max_y or self.x >= self.max_x:
            self.group.remove(self)
