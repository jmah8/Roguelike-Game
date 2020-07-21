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

    def __init__(self, name_instance, hp, killable=None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.owner = None
        self.killable = killable

    def take_damage(self, damage):
        """
        Creature takes damage to hp and if hp is <= 0 and killable == True, it dies
        """
        self.hp -= damage
        self.owner.game.print_game_message(
            self.name_instance + " took " + str(damage) + " damage", RED)
        self.owner.game.print_game_message(
            self.name_instance + "'s hp is at :" + str(self.hp), WHITE)

        if self.hp <= 0 and self.killable:
            self.die()
            

    def die(self):
        """
        Prints that object is dead and removes it from all_creature and enemies group
        """
        self.owner.game.print_game_message(
            self.name_instance + " is dead", BLUE)
        self.owner.game.all_creature.remove(self.owner)
        self.owner.game.enemies.remove(self.owner) 

    def move(self, dx, dy):
        """
        Moves entity's position if tile is not a tile or enemy
        else do nothing if wall or attack if enemy

        Moves entity by dx and dy on map. If entity collides with
        wall or enemy, stop it from moving by actually reversing the move

        Arg:
            dx (arg, int): int to change entity's x coord
            dy (arg, int): int to change entity's y coord
        """
        # For animation
        if (dx > 0):
            self.owner.right = True
            self.owner.left = False
            self.owner.moving = True
        elif (dx < 0):
            self.owner.right = False
            self.owner.left = True
            self.owner.moving = True

        self.owner.x += dx
        self.owner.y += dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)


        # check to see if entity collided with wall and if so don't move
        creature_collide_with_wall = pygame.sprite.spritecollideany(
            self.owner, self.owner.game.walls)

        if creature_collide_with_wall:
            self.reverse_move(dx, dy)


        # check to see if entity (player) collided with enemy and if so don't move
        if_player = self.owner.game.player_group.has(self.owner)

        if if_player:
            creature_hit = pygame.sprite.spritecollideany(
                self.owner, self.owner.game.enemies)
            if creature_hit:
                self.reverse_move(dx, dy)
                self.attack(creature_hit, 1)


        # check to see if entity (enemy) collided with player and if so don't move
        if_enemy = self.owner.game.enemies.has(self.owner)

        if if_enemy:
            creature_hit = pygame.sprite.spritecollideany(
                self.owner, self.owner.game.player_group)
            if creature_hit:
                self.reverse_move(dx, dy)
                self.attack(creature_hit, 1)

    def reverse_move(self, dx, dy):
        """
        Reverse the move

        Arg:
            dx (arg, int): int to change entity's x coord
            dy (arg, int): int to change entity's y coord
        """
        self.owner.x -= dx
        self.owner.y -= dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

    def attack(self, target, damage):
        """
        Attack target creature for damage

        Arg:
            target (arg, object): object to attack
            damage (arg, int): damage to do to object
        """
        self.owner.game.print_game_message(self.name_instance + " attacks " + target.creature.name_instance
                                           + " for " + str(damage) + " damage", WHITE)
        target.creature.take_damage(damage)

class ai_test:
    """
    Once per turn, execute
    """
    def __init__(self):
        self.owner = None

    def take_turn(self):
        """
        Make creature move towards the player if in creature FOV,
        else wander
        """
        diff_x = self.owner.x - self.owner.game.player.x
        diff_y = self.owner.y - self.owner.game.player.y

        # If player is not in enemy FOV wander
        if (abs(diff_x) > SLIME_FOV or abs(diff_y) > SLIME_FOV):
            self.owner.creature.move(random.choice(
                [0, 1, -1]), random.choice([0, 1, -1]))
        # Else move towards player using shortest path
        else:
            move_x = self._calculate_change_in_position(diff_x)
            move_y = self._calculate_change_in_position(diff_y)

            self.owner.creature.move(move_x, move_y)

    def _calculate_change_in_position(self, diff):
        """
        Helper function for take_turn. Returns int that moves
        self closer to player

        Arg:
            diff (int, arg): difference between self position and player
        """
        if (diff > 0):
            move = -1
        elif (diff < 0):
            move = 1
        else:
            move = 0
        return move


class container:
    def __init__(self, volume=10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume


    ## TODO Get Name Inventory()
    ## TODO Get volume of container()
    ## TODO get weight of inventory()

class Item:
    def __init__(self, weight = 0.0, volume = 0.0):
        self.weight = weight
        self.volume = volume

    ## TODO pickup_item()
    '''
    Entity (Player/Creature Object) picks up item
    '''
    def pickup_item(self, entity):
        if entity.container:
            if entity.container.volume + self.volume > entity.container.max_volume:
                entity.game.print_game_message("Inventory Full", WHITE)
            else:
                entity.game.print_game_message("Picked Up ####")
                entity.container.inventory.append(self.owner)
                self.container = entity.container

                # need game object first
                # game.current_objects.remove(self.owner)


    ## TODO drop_item()
    def drop_item(self, entity):
        # game.current_objects.append(self.owner)
        self.container.inventory.remove(self.owner)
        entity.game.print_game_message("#### Item Dropped")
        
        ## TODO use_item()
