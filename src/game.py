import os
import pygame

# Variables
RESOLUTION = (1216, 640)
SPRITE_SIZE = 64
TOPLEFT = (0, 0)

# Code
class tile:
    def __init__(self, walkable):
        self.walkable = walkable

def create_map():
    create_map = [[ tile(True) for y in range(0, (RESOLUTION[1] // SPRITE_SIZE))] for x in range(0, (RESOLUTION[0] // SPRITE_SIZE))]

    create_map[1][2].walkable = False
    create_map[3][4].walkable = False

    return create_map

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
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage('16x16/heroes/knight/knight_idle_anim_f0.png', -1)
        self.health = 3
        self.position = (800, 320)

    def update(self):
        self.rect.move()

def draw_game():
    global SURFACE_MAIN, PLAYER

    draw_map(MAP)

    PLAYER = Player()
    SURFACE_MAIN.blit(PLAYER.image, PLAYER.position)

    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, (RESOLUTION[0] // SPRITE_SIZE)):
        for y in range(0, (RESOLUTION[1] // SPRITE_SIZE)):
            if map_to_draw[x][y].walkable == True:
                floor = loadImage('16x16/tiles/floor/floor_1.png')
                SURFACE_MAIN.blit(floor[0], (x * SPRITE_SIZE, y * SPRITE_SIZE))
            else:
                wall = loadImage('16x16/tiles/wall/wall_1.png')
                SURFACE_MAIN.blit(wall[0], (x * SPRITE_SIZE, y * SPRITE_SIZE))
    pygame.display.flip()

def main_loop():
    #TODO: Maybe get rid of global variables later
    global SURFACE_MAIN, PLAYER, BACKGROUND
    draw_game()
    position = PLAYER.rect.move(PLAYER.position)
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            # SURFACE_MAIN.blit(MAP[0], position, position)
            if event.type == pygame.QUIT:
                run = False
                break
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         position = position.move(-PLAYER.velocity_x, 0)
            #     elif event.key == pygame.K_d:
            #         position = position.move(PLAYER.velocity_x, 0)
            #     elif event.key == pygame.K_s:
            #         position = position.move(0, PLAYER.velocity_y)
            #     elif event.key == pygame.K_w:
            #         position = position.move(0, -PLAYER.velocity_y)
            #     SURFACE_MAIN.blit(PLAYER.image, position)
            #     pygame.display.flip()
            #     pygame.time.delay(10)
    pygame.quit()
    exit()

def init():
    global SURFACE_MAIN, MAP

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('My Pygame')

    MAP = create_map()


if __name__ == '__main__':
    init()
    main_loop()