import pygame
import os

pygame.init()

def loadImage(name, colorkey=None):
    pathname = os.path.join('resource', name)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(name)
    image = image.convert()
    image = pygame.transform.scale(image, (64, 64))
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()



# TODO: change path for images to constant when right picture is found
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('16x16/heroes/knight/knight_idle_anim_f0.png', -1)
        self.health = 3
        self.position = (800, 320)

    def update(self):
        self.rect.move()