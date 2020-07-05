import os
import pygame

# Variables
RESOLUTION = (1200, 600)
VELOCITY = 20
TOPLEFT = (0, 0)
PLAYERSTART = (800, 400)

# Code
def loadImage(name, colorkey=None):
    pathname = os.path.join('resource', name)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(name)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('Player.png', -1)
        self.image
        self.health = 3
        self.velocity = (0, 0)
        self.position = (800, 400)

    def update(self):
        self.rect.move(velocity)



pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('My Pygame')


background = loadImage('Background.jpg')
screen.blit(background, TOPLEFT)

player = loadImage('Player.png')
screen.blit(player, PLAYERSTART)


position = player.get_rect().move(PLAYERSTART)

pygame.display.flip()

run = True
while run:
    events = pygame.event.get()
    for event in events:
        screen.blit(background, position, position)
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                position = position.move(-VELOCITY, 0)
            elif event.key == pygame.K_d:
                position = position.move(VELOCITY, 0)
            elif event.key == pygame.K_s:
                position = position.move(0, VELOCITY)
            elif event.key == pygame.K_w:
                position = position.move(0, -VELOCITY)
            screen.blit(player, position)
            pygame.display.flip()
            pygame.time.delay(10)

pygame.quit()