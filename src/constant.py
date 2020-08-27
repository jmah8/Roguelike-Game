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

# Player
HP_BAR_WIDTH = SPRITE_SIZE * 3
HP_BAR_HEIGHT = SPRITE_SIZE / 3
MP_BAR_WIDTH = SPRITE_SIZE * 3
MP_BAR_HEIGHT = SPRITE_SIZE / 3
EXP_BAR_WIDTH = SPRITE_SIZE * 3
EXP_BAR_HEIGHT = SPRITE_SIZE / 6

# Map gen constants
READ_FROM_FILE = False
MAP_WIDTH = 20
MAP_HEIGHT = 20
SUB_DUNGEON_WIDTH = 8
SUB_DUNGEON_HEIGHT = 8
DIST_FROM_SISTER_NODE_MIN = 2
# DIST_FROM_SISTER_NODE_MAX * 2 has to be <= SUB_DUNGEON WIDTH/HEIGHT
DIST_FROM_SISTER_NODE_MAX = 3

# Minimap constants
MINIMAP_SCALE = 2

# Button manager constants
NUM_OF_BUTTONS = 4

# Console map output
WALL = '1'
FLOOR = '.'
PATH = '0'
DOWNSTAIR = '>'
UPSTAIR = '<'

# Colours
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
INVENTORY_BEIGE = (239,228,176)

# Game constants
NUM_OF_FLOOR = 3

# Creature stats
REGEN_TIME = 5

# Enemy Attributes
# FOV should be 1 bigger than actual FOV since player acts first
# and so player can move out of enemy FOV before enemy acts
SLIME_FOV = 3

# Resource path
RESOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource')

#Save path
SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/save.txt')

# Image path
KNIGHT = 'creatures/knight/knight_idle_anim_f0.png'
KNIGHT_RUN = 'creatures/knight/knight_run_anim_f0.png'

SLIME = 'creatures/slime/slime_idle_anim_f0.png'
SLIME_RUN = 'creatures/slime/slime_run_anim_f0.png'

GOBLIN = 'creatures/goblin/goblin_idle_anim_f0.png'
GOBLIN_RUN = 'creatures/goblin/goblin_run_anim_f0.png'

SKELETON = 'creatures/skeleton/skelet_idle_anim_f0.png'
SKELETON_RUN = 'creatures/skeleton/skelet_run_anim_f0.png'

SPIKE = 'tiles/floor/spikes_anim_f0.png'
SPIKE_1 = 'tiles/floor/spikes_anim_f6.png'

FLOOR_1 = 'tiles/floor/floor_1.png'
FLOOR_2 = 'tiles/floor/floor_2.png'
FLOOR_3 = 'tiles/floor/floor_3.png'
FLOOR_4 = 'tiles/floor/floor_4.png'
FLOOR_5 = 'tiles/floor/floor_side2.png'
FLOOR_6 = 'tiles/floor/floor_side3.png'
FLOOR_7 = 'tiles/floor/floor_side4.png'
FLOOR_8 = 'tiles/floor/floor_side5.png'

STAIR_UP = 'tiles/stair_prevlevel.png'
STAIR_DOWN = 'tiles/stair_nextlevel.png'

WALL_1 = 'tiles/wall/wall_1.png'
RED_POTION = 'items/consumables/potion_red.png'
SWORD = 'items/sword.png'

INVENTORY = 'ui/chest_closed_anim_f2.png'
EMPTY_INVENTORY_SLOT = 'items/empty_inventory_slot.png'
MOUSE_SELECT = 'ui/mouse_select.png'
MINIMAP_BUTTON = 'ui/minimap.png'

EQUIP_SCREEN = 'items/equipment_screen.png'

FIREBALL = 'magic/fireball.png'
LIGHTNING = 'magic/lightning.png'

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
