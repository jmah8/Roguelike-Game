import random
from constant import *
import gamemap
import pygame

class creature:
    """
    have hp
    can damage other objects
    can die

    Attributes:
        name_instance (arg, string) : Name of creature
        hp (arg, int) : HP of creature
        owner (object) : object that has self as creature component
    """

    def __init__(self, name_instance, hp, death_function = None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.owner = None
        self.death_function = death_function

    def take_damage(self, damage):
        """
        Creature takes damage to hp and if hp is <= 0, it dies
        """
        self.hp -= damage
        print (self.name_instance + " took " + str(damage) + " damage")
        print (self.name_instance + "'s hp is at :" + str(self.hp))

        if self.hp <= 0 and self.death_function:
            self.death_function(self.owner)

    def move(self, dx, dy, game):
        """
        Moves entity's position if tile is walkable else do nothing

        Moves entity by dx and dy on map

        Arg:
            dx (arg, int): int to change entity's x coord
            dy (arg, int): int to change entity's y coord
            map (arg, array[array]): map when entity is
        """
        self.owner.x += dx
        self.owner.y += dy
        self.owner.rect.topleft = (self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)
        if pygame.sprite.spritecollideany(self.owner, game.walls):
            self.owner.x -= dx
            self.owner.y -= dy
            self.owner.rect.topleft = (self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)
        if game.player_group.has(self.owner):
            enemy_hit = pygame.sprite.spritecollideany(self.owner, game.enemies)
            if  enemy_hit:
                self.owner.x -= dx
                self.owner.y -= dy
                self.owner.rect.topleft = (self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)
                self.attack(enemy_hit, 1)
        if game.enemies.has(self.owner):
            enemy_hit = pygame.sprite.spritecollideany(self.owner, game.player_group)
            if  enemy_hit:
                self.owner.x -= dx
                self.owner.y -= dy
                self.owner.rect.topleft = (self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)
                self.attack(enemy_hit, 1)


    def attack(self, target, damage):
        """
        Attack target creature for damage

        Arg:
            target (arg, object): object to attack
            damage (arg, int): damage to do to object
        """
        print(self.name_instance + " attacks " + target.creature.name_instance 
        + " for " + str(damage)  + " damage")
        target.creature.take_damage(damage)


def death(obj):
    """
    Creature death. Remove creature from groups and stop drawing it
    """
    print (obj.creature.name_instance + " is dead")
    obj.game.all_sprites.remove(obj)
    obj.game.enemies.remove(obj)






class ai_test:
    """
    Once per turn, execute
    """
    def __init__(self):
        self.owner = None

    def takeTurn(self, game):
        self.owner.creature.move(random.choice([0, 1, -1]),
                        random.choice([0, 1, -1]), game)

# class item:
# class container:
