from constant import WHITE, SPRITE_SIZE


class Item:
    def __init__(self, name, weight=0.0, volume=0.0, consumable=None):
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
                game.add_game_message_to_print("Inventory Full", WHITE)
            else:
                game.add_game_message_to_print("Picked Up " + self.name, WHITE)
                entity.container.inventory.append(self.owner)

                entity.game.item_group.remove(self.owner)

    def drop_item(self, entity, x, y):
        """
        Drop item and position x and y
        Update position and rect of item to player.x,player,y
        Remove item from inventory
        Add item to game_objects
        """
        self.owner.game.item_group.insert(0, self.owner)
        entity.container.inventory.remove(self.owner)
        self.owner.x = x
        self.owner.y = y
        self.owner.rect.topleft = (x * SPRITE_SIZE, y * SPRITE_SIZE)
        game.add_game_message_to_print(self.name + " Item Dropped", WHITE)

    ## TODO use_item()