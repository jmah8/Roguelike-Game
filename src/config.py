from constant import *
import pygame
import sprite
import gamemap
import camera
import pathfinding

pygame.init()

SURFACE_MAIN = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
CLOCK = pygame.time.Clock()
# Load in all the sprites
SPRITE = sprite.GameSprites()
# Initialized in game.new
MAP_INFO = None
CAMERA = None
PATHFINDING = None

PLAYER = None

TURN_COUNT = 0