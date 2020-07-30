import random
from constant import *
import gamemap
import pygame


class Creature:
    """
    have hp
    can damage other objects
    can die

    Attributes:
        name_instance (arg, string) : Name of creature
        hp (arg, int) : HP of creature
        owner (object) : object that has self as creature component
        killable (arg, boolean) : if creature is killable
        enemy_group (arg, group): group creature can attack
        walk_through_tile (arg, boolean): if creature can walk through tiles like walls
    """

    def __init__(self, name_instance, hp, killable=None, enemy_group=None, walk_through_tile=False):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.owner = None
        self.killable = killable
        self.enemy_group = enemy_group
        self.walk_through_tile = walk_through_tile

    def take_damage(self, damage):
        """
        Creature takes damage to hp and if hp is <= 0 and killable == True, it dies
        """
        self.hp -= damage
        self.owner.game.drawing.print_game_message(
            self.name_instance + " took " + str(damage) + " damage", RED)
        self.owner.game.drawing.print_game_message(
            self.name_instance + "'s hp is at :" + str(self.hp), WHITE)

        if self.hp <= 0 and self.killable:
            self.die()
            

    def die(self):
        """
        Prints that object is dead and removes it from all_creature and enemies group
        """
        self.owner.game.drawing.print_game_message(
            self.name_instance + " is dead", BLUE)
        self.owner.game.all_creature.remove(self.owner)
        self.owner.game.GAME_OBJECTS.remove(self.owner)
        self.owner.game.enemy_group.remove(self.owner)

    def move(self, dx, dy):
        """
        Moves entity's position if tile is not a tile or enemy
        else do nothing if wall or attack if enemy

        Moves entity by dx and dy on map. If entity collides with
        wall or enemy, stop it from moving by actually reversing the move

        Args:
            dx (int): int to change entity's x coord
            dy (int): int to change entity's y coord
        """
        self._update_anim_status(dx, dy)

        self.owner.x += dx
        self.owner.y += dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

        if (not self.walk_through_tile):
            # check to see if entity collided with wall and if so don't move
            creature_collide_with_wall = pygame.sprite.spritecollideany(
                self.owner, self.owner.game.walls)

            if creature_collide_with_wall:
                self.reverse_move(dx, dy)

        # check to see if entity collided with enemy and if so don't move
        if (self.enemy_group):
            creature_hit = pygame.sprite.spritecollideany(self.owner, self.enemy_group)
            if creature_hit:
                self.reverse_move(dx, dy)
                self.attack(creature_hit, 1)


    def _update_anim_status(self, dx, dy):
        """
        Updates the direction the sprite is moving

        If sprite is moving regardless of direction, moving is true.
        If sprite is moving left, left = True and right = False and
        opposite is true for moving right

        Args:
            dx (int): change in x
            dy (int): change in y
        """
        if (dx > 0):
            self.owner.right = True
            self.owner.left = False
            self.owner.moving = True
        elif (dx < 0):
            self.owner.right = False
            self.owner.left = True
            self.owner.moving = True
        
        if (not dy == 0):
            self.owner.moving = True


    def reverse_move(self, dx, dy):
        """
        Reverse the move

        Args:
            dx (int): int to change entity's x coord
            dy (int): int to change entity's y coord
        """
        self.owner.x -= dx
        self.owner.y -= dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

    def attack(self, target, damage):
        """
        Attack target creature for damage

        Args:
            target (object): object to attack
            damage (int): damage to do to object
        """
        self.owner.game.drawing.print_game_message(self.name_instance + " attacks " + target.creature.name_instance
                                           + " for " + str(damage) + " damage", WHITE)
        target.creature.take_damage(damage)

class Ai_test:
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

        Args:
            diff (int): difference between self position and player
        """
        if (diff > 0):
            move = -1
        elif (diff < 0):
            move = 1
        else:
            move = 0
        return move


class Container:
    def __init__(self, volume=10.0, inventory = []):
        self.inventory = inventory
        self.volume = volume


    ## TODO Get Name Inventory()
    ## TODO Get volume of container()
    ## TODO get weight of inventory()

class Item:
    def __init__(self, name, weight = 0.0, volume = 0.0, consumable = None):
        self.name = name
        self.weight = weight
        self.volume = volume
        self.owner = None

    '''
    Entity (Player/Creature Object) with container picks up item if
    the current volume of container + item is < container.volume
    Add item to inventory
    Remove item from game_objects 
    '''
    def pick_up(self, entity):
        if entity.container:
            if entity.container.volume + self.volume > entity.container.volume:
                self.owner.game.drawing.print_game_message("Inventory Full", WHITE)
            else:
                self.owner.game.drawing.print_game_message("Picked Up " + self.name, WHITE)
                entity.container.inventory.append(self.owner)

                entity.game.GAME_OBJECTS.remove(self.owner)

    def drop_item(self, entity, x, y):
        """
        Drop item and position x and y
        Update position and rect of item to player.x,player,y
        Remove item from inventory
        Add item to game_objects
        """
        self.owner.game.GAME_OBJECTS.insert(0, self.owner)
        entity.container.inventory.remove(self.owner)
        self.owner.x = x
        self.owner.y = y
        self.owner.rect.topleft = (x*SPRITE_SIZE,y*SPRITE_SIZE)
        self.owner.game.drawing.print_game_message(self.name + " Item Dropped", WHITE)

    ## TODO use_item()
