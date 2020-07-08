import os
import pygame
import constant

pygame.init()

def loadImage(name, colorkey=None):
    '''
    Load and convert image to surface and returns image and the image rect
    and makes color at colorkey transparent
    Arg:
        name (arg, string) : Pathname of image to convert
        colorkey (arg, (int, int)) : Position of color to be transparent
    '''
    pathname = os.path.join('resource', name)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(name)
    # convert_alpha() is also an option
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (64, 64))
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()





class object(pygame.sprite.Sprite):
    '''
    Class for object which represents entity, which is anything that appears
    and acts in the game

    Attributes:
        x (arg, int): Position on x axis
        y (arg, int): Position on y axis
        image (arg, string): Path to image of entity
    '''

    def __init__(self, x, y, object_id, image, creature=None, ai=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage(image, -1)
        self.x = x
        self.y = y
        self.rect.move_ip(self.x*constant.SPRITE_SIZE, self.y*constant.SPRITE_SIZE)
        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw_object(self, surface):
        '''
        Draws entity image to surface at entity's position

        Draws entity on coord taking into account the size of the sprites

        Arg:
            surface (arg, pygame.surface): surface to draw image on
        '''
        surface.blit(self.image, (self.x*constant.SPRITE_SIZE, self.y*constant.SPRITE_SIZE))

    def move(self, dx, dy, map):
        '''
        Moves entity's position if tile is walkable else do nothing

        Moves entity by dx and dy on map

        Arg:
            dx (arg, int): int to change entity's x coord
            dy (arg, int): int to change entity's y coord
            map (arg, array[array]): map when entity is
        '''
        if map[self.x + dx][self.y + dy].walkable == True:
           self.x += dx
           self.y += dy 
           self.rect = self.rect.move(dx*constant.SPRITE_SIZE, dy*constant.SPRITE_SIZE)

    def update(self):
        pass


# # TODO: change path for images to constant when right picture is found
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image, self.rect = loadImage(
#             '16x16/heroes/knight/knight_idle_anim_f0.png', -1)
#         self.health = 3
#         self.position = (5, 3)

#     def update(self):
#         pass

# TODO: change path for images to constant when right picture is found
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('16x16/heroes/knight/knight_idle_anim_f0.png', -1)
        self.health = 3
        self.position = (5, 3)

# class Slime(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image, self.rect = loadImage(
#             '16x16/mobs/slime_idle_anim_f0.png', -1)
#         self.health = 3
#         self.position = (5, 3)

#     def update(self):
#         pass
