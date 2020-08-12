import pygame
import os

pygame.font.init()

# Display constants
# Amount of tiles on screen
TILE_WIDTH = 16
TILE_HEIGHT = 12

SPRITE_SIZE = 64
CAMERA_WIDTH = TILE_WIDTH * SPRITE_SIZE
CAMERA_HEIGHT = TILE_HEIGHT * SPRITE_SIZE
RESOLUTION = (CAMERA_WIDTH, CAMERA_HEIGHT)
TOPLEFT = (0, 0)

# Map gen constants
READ_FROM_FILE = False
MAP_WIDTH = 50
MAP_HEIGHT = 40
SUB_DUNGEON_WIDTH = 4
SUB_DUNGEON_HEIGHT = 4
DIST_FROM_SISTER_NODE_MIN = 1
# DIST_FROM_SISTER_NODE_MAX * 2 has to be <= SUB_DUNGEON WIDTH/HEIGHT
DIST_FROM_SISTER_NODE_MAX = 1

# Minimap constants
MINIMAP_SCALE = 2

# Button manager constants
NUM_OF_BUTTONS = 3


# Console map output
WALL = '1'
FLOOR = '.'
PATH = '0'

# Colours
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
INVENTORY_BEIGE = (239,228,176)


# Enemy Attributes
# FOV should be 1 bigger than actual FOV since player acts first
# and so player can move out of enemy FOV before enemy acts
SLIME_FOV = 3

# Resource path
RESOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')


# Image path
KNIGHT = 'knight/knight_idle_anim_f0.png'
KNIGHT_RUN = 'knight/knight_run_anim_f0.png'

SLIME = 'slime/slime_idle_anim_f0.png'
SLIME_RUN = 'slime/slime_run_anim_f0.png'

SPIKE = '16x16/tiles/floor/spikes_anim_f0.png'
SPIKE_1 = '16x16/tiles/floor/spikes_anim_f6.png'

FLOOR_1 = '16x16/tiles/floor/floor_1.png'
FLOOR_2 = '16x16/tiles/floor/floor_2.png'
FLOOR_3 = '16x16/tiles/floor/floor_3.png'
FLOOR_4 = '16x16/tiles/floor/floor_4.png'
FLOOR_5 = '16x16/tiles/floor/floor_side2.png'
FLOOR_6 = '16x16/tiles/floor/floor_side3.png'
FLOOR_7 = '16x16/tiles/floor/floor_side4.png'
FLOOR_8 = '16x16/tiles/floor/floor_side5.png'

WALL_1 = '16x16/tiles/wall/wall_1.png'
RED_POTION = 'items/consumables/potion_red.png'
SWORD = 'items/sword.png'

INVENTORY = 'ui/chest_closed_anim_f2.png'
EMPTY_INVENTORY_SLOT = 'items/empty_inventory_slot.png'
MOUSE_SELECT = 'ui/mouse_select.png'
MINIMAP_BUTTON = 'ui/minimap.png'

EQUIP_SCREEN = 'items/equipment_screen.png'

FIREBALL = 'magic/fireball.png'

# FONTS
font_path_name = os.path.join(RESOURCE_PATH, 'fonts/FFF_Tusj.ttf')
FONT_SIZE = 28
FONT_DEBUG_MESSAGE = pygame.font.Font(font_path_name, 28)
FONT_MESSAGE_TEXT = pygame.font.Font(font_path_name, 28)
TEXT_SPACE_BUFFER = 5

# MESSAGE DEFAULTS
NUM_MESSAGES = 8

# ANIMATIONS
ANIMATION_SPEED = 0.75
FPS = 60

# RAYCASTING
RAYS = 360
STEP = 3
KNIGHT_FOV = 3
