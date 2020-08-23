from constant import *
import pygame
import sprite
import entity_generator
import gamemap
import camera
import pathfinding
import fov

pygame.init()

SURFACE_MAIN = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
CLOCK = pygame.time.Clock()
# Load in all the sprites
SPRITE = sprite.GameSprites()

MAP_INFO = gamemap.MapInfo()
CAMERA = camera.Camera(MAP_INFO)
PATHFINDING = pathfinding.Graph()
PATHFINDING.make_graph(MAP_INFO)
PATHFINDING.neighbour()

PLAYER = None

FOV = fov.new_fov(MAP_INFO)

TURN_COUNT = 0