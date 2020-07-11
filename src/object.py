import os
import pygame
from constant import *
from sprite import *



pygame.init()



class object(pygame.sprite.Sprite):
    """
    Class for object which represents entity, which is anything that appears
    and acts in the game

    Attributes:
        game (arg, game): Game with all game data
        x (arg, int): Position on x axis
        y (arg, int): Position on y axis
        object_id (arg, string): id of object
        image (arg, sprite): Sprite of image
        creature (arg, creature): Creature it is
        ai (arg, ai): Ai object has
    """

    def __init__(self, game, x, y, object_id, image, creature=None, ai=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.l_image = pygame.transform.flip(self.image, True, False)
        self.r_image = self.image
        self.object_id = object_id
        self.x = x
        self.y = y 
        self.rect.topleft = (self.x*SPRITE_SIZE, self.y*SPRITE_SIZE)
        
        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self


    def update(self, dx, dy):
        """
        Updates the object depending on its ai or player input
        """
        if self.ai:
            self.ai.takeTurn()
        elif self.game.player_group.has(self):
            self.creature.move(dx, dy)



