import pygame
import pygame.freetype
from constant import *
import drawing

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
        v_x (int): x velocity of particle
        v_y (int): y velocity of particle
        max_x (int): max x position of particle (after which it disappears)
        max_y (int): max y position of particle (after which it disappears)
        group (arg, Group): group particle belongs to
    """

    # TODO: add check for when actual map is smaller than RESOLUTION,
    #       so x and y aren't in sync just like the mouse cursor
    def __init__(self, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * SPRITE_SIZE
        self.y = y * SPRITE_SIZE
        self.group = group
        # self.v_x = 2
        # self.v_y = -5
        # self.max_x = self.x
        # self.max_y = self.y
        # self.image, self.rect = myfont.render("1", RED)
        # self.rect.x = x
        # self.rect.y = y
        # self.group = group


class DamageNumParticle(Particle):
    def __init__(self, x, y, damage, group):
        Particle.__init__(self, x, y, group)
        self.v_x = 2
        self.v_y = -5
        self.max_x = self.x + SPRITE_SIZE
        self.max_y = self.y
        self.image, self.rect = myfont.render(str(damage), RED)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.x += self.v_x
        self.y += self.v_y
        self.v_y += 0.25
        if self.y >= self.max_y or self.x >= self.max_x:
            self.group.remove(self)
