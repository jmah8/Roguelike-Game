from game import *
import pygame

game = Game()
while game.running:
    game.new()
    game.run()
pygame.quit()
