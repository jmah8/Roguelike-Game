
class creature:
    '''
    have hp
    can damage other objects
    can die
    '''
    def __init__(self,name_instance, hp =10):

        self.name_instance = name_instance
        self.hp = hp
        self.owner = None

# class item:
# class container:


class ai:
    '''
    Once per turn execute
    '''
    def take_turn(self):
        self.owner.move(-1, 0);

