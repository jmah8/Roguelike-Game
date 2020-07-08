import os
import pygame
import map
import constant
import object
import components
import game

class creature:
    '''
    have hp
    can damage other objects
    can die
    '''

    def __init__(self, name_instance, hp=10):

        self.name_instance = name_instance
        self.hp = hp


class ai_test:
    '''
    Once per turn, execute
    '''

    def takeTurn(self):
        self.owner.move(-1, 0, constant.com_map)

# class item:
# class container:
