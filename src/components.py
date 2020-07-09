import random
import constant

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
        self.hp -= damage
        print (self.name_instance + " took " + str(damage) + " damage")
        print (self.name_instance + "'s hp is at :" + str(self.hp))

        if self.hp <= 0 and self.death_function:
            self.death_function(self.owner)


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
        self.owner.move(random.choice([0, 1, -1]),
                        random.choice([0, 1, -1]), constant.com_map)

# class item:
# class container:
