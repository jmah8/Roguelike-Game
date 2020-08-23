from constant import *
import pygame
import sprite
import gamemap

pygame.init()

SURFACE_MAIN = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
CLOCK = pygame.time.Clock()
SPRITE = sprite.GameSprites()
MAP_INFO = None
PLAYER = None