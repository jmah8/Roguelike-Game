import random
import constant

class creature:
    '''
    have hp
    can damage other objects
    can die

    Attributes:
        name_instance (arg, string) : Name of creature
        hp (arg, int) : HP of creature
        owner (object) : object that has self as creature component
    '''

    def __init__(self, name_instance, hp=10):
        self.name_instance = name_instance
        self.hp = hp
        self.owner = None


class ai_test:
    '''
    Once per turn, execute
    '''
    def __init__(self):
        self.owner = None

    def takeTurn(self):
        self.owner.move(random.choice([0, 1, -1]),
                        random.choice([0, 1, -1]), constant.com_map)

# class item:
# class container:
