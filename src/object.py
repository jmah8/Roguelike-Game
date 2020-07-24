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

    def __init__(self, game, x, y, object_id, image=None, anim=None, creature=None, ai=None, container = None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y 
        self.object_id = object_id
        self.anim = anim
        self.image = image
        if not self.image:
            self.image = anim['idle_right'][0]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x*SPRITE_SIZE, self.y*SPRITE_SIZE)

        self.left = False
        self.right = True
        self.moving = False

        # TODO: Refactor this to a new class later
        if (anim):
            self.flicker_speed = ANIMATION_SPEED / len(self.anim) / 1.0
            self.flicker_timer = 0.0
            self.anim_frame = 0     


        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def update_anim(self):
        """
        Updates objects sprite depending on time passed
        """
        if (self.anim):
            clock = self.game.clock.get_fps()

            if clock > 0.0:
                self.flicker_timer += 1 / clock
            
            if self.flicker_timer >= self.flicker_speed:
                self.flicker_timer = 0.0

                if self.anim_frame >= len(self.anim) - 1:
                    self.anim_frame = 0
                    self.moving = False

                else:
                    self.anim_frame += 1
                    self.moving = False

            if self.right:
                if self.moving:
                    self.image = self.anim["run_right"][self.anim_frame]
                else:
                    self.image = self.anim["idle_right"][self.anim_frame]
            else:
                if self.moving:
                    self.image = self.anim["run_left"][self.anim_frame]
                else:
                    self.image = self.anim["idle_left"][self.anim_frame]

            # self.moving = False
                

    def update(self, dx, dy):
        """
        Updates the object depending on its ai or player input
        """
        if self.ai:
            self.ai.take_turn()
        else:
            self.creature.move(dx, dy)
            print(self.x)
            print(self.y)
            print(self.rect.x)
            print(self.rect.y)
