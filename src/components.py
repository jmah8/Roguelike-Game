import random
import constant
import gamemap

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

    def move(self, dx, dy, map):
        """
        Moves entity's position if tile is walkable else do nothing

        Moves entity by dx and dy on map

        Arg:
            dx (arg, int): int to change entity's x coord
            dy (arg, int): int to change entity's y coord
            map (arg, array[array]): map when entity is
        """
        target = gamemap.check_map_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)

        is_walkable_tile = map[self.owner.x + dx][self.owner.y + dy].walkable == True

        if  is_walkable_tile and target is None:
            self.owner.x += dx
            self.owner.y += dy
            self.owner.rect = self.owner.rect.move(dx*constant.SPRITE_SIZE, dy*constant.SPRITE_SIZE)

        if target:
            self.attack(target, 1)


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
    Creature death. First option results in removing the sprite,
    but second option leaves sprite in 
    """
    print (obj.creature.name_instance + " is dead")
    # Remove creature
    constant.game_objects.remove(obj.creature.owner)
    # Leave creature
    # obj.creature = None
    # obj.ai = None






class ai_test:
    """
    Once per turn, execute
    """
    def __init__(self):
        self.owner = None

    def takeTurn(self):
        self.owner.creature.move(random.choice([0, 1, -1]),
                        random.choice([0, 1, -1]), constant.com_map)

# class item:
# class container:
