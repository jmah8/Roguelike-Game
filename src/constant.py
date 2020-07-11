import pygame
pygame.font.init()

# Display constants
TILE_WIDTH = 16
TILE_HEIGHT = 12
SPRITE_SIZE = 64
MAP_WIDTH = TILE_WIDTH * SPRITE_SIZE
MAP_HEIGHT = TILE_HEIGHT * SPRITE_SIZE
RESOLUTION = (MAP_WIDTH, MAP_HEIGHT)
TOPLEFT = (0, 0)

# Colours
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (255,255,255)
WHITE = (0,0,0)
# Enemy Attributes
# FOV should be 1 bigger than actual FOV since player acts first
# and so player can move out of enemy FOV before enemy acts
SLIME_FOV = 3

# Image path
PLAYER = '16x16/heroes/knight/knight_idle_anim_f0.png'
SLIME = 'mobs/slime_idle_anim_f0.png'

FLOOR_1 = '16x16/tiles/floor/floor_1.png'
FLOOR_2 = '16x16/tiles/floor/floor_2.png'
FLOOR_3 = '16x16/tiles/floor/floor_3.png'
FLOOR_4 = '16x16/tiles/floor/floor_4.png'
FLOOR_5 = '16x16/tiles/floor/floor_side2.png'
FLOOR_6 = '16x16/tiles/floor/floor_side3.png'
FLOOR_7 = '16x16/tiles/floor/floor_side4.png'
FLOOR_8 = '16x16/tiles/floor/floor_side5.png'

WALL_1 = '16x16/tiles/wall/wall_1.png'

FPS = 60

#FONTS
FONT_DEBUG_MESSAGE = pygame.font.Font('resource/fonts/FFF_Tusj.ttf', 28)