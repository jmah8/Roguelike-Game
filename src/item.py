from constant import *
import config
import game_text
import entity_generator

class Item:
    def __init__(self, name, weight=0.0, volume=0.0):
        self.name = name
        self.weight = weight
        self.volume = volume
        self.owner = None
        self.current_container = None

    '''
    Entity (Player/Creature Object) with container picks up item if
    the current volume of container + item is < container.volume
    Add item to inventory
    Remove item from game_objects 
    '''

    def pick_up(self, entity):
        if entity.container:
            if entity.container.volume + self.volume > entity.container.volume:
                game_text.add_game_message_to_print("Inventory Full", WHITE)
            else:
                game_text.add_game_message_to_print("Picked Up " + self.name, WHITE)
                entity.container.inventory.append(self.owner)

                config.GAME_DATA.item_data.remove(self.owner)

                self.current_container = entity.container

    def drop_item(self, entity, x, y):
        """
        Drop item and position x and y
        Update position and rect of item to player.x,player,y
        Remove item from inventory
        Add item to game_objects
        """
        config.GAME_DATA.item_data.insert(0, self.owner)
        entity.container.inventory.remove(self.owner)
        self.current_container = None
        self.owner.x = x
        self.owner.y = y
        game_text.add_game_message_to_print(self.name + " Item Dropped", WHITE)

    def use_item(self):
        """
        Uses item and produces effect and removes it
        """
        use_fn = item_use_dict[self.name]
        if use_fn:
            use_fn(self.current_container.owner)
            self.current_container.inventory.remove(self.owner)
            self.current_container = None


def heal_user_hp(user_entity):
    user_entity.creature.stat.heal_hp(10)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(10) + " hp",
                                        WHITE)


def heal_user_mp(user_entity):
    user_entity.creature.stat.heal_mp(5)
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " healed " + str(5) + " mp",
                                        WHITE)


def teleport_user(user_entity):
    x, y = entity_generator.generate_player_spawn(config.MAP_INFO.map_tree)
    user_entity.x, user_entity.y = x, y
    game_text.add_game_message_to_print(user_entity.creature.name_instance + " teleported",
                                        BLUE)


# Lookup table for item effect when used
item_use_dict = {
    "Red Potion": heal_user_hp,
    "Blue Potion": heal_user_mp,
    "Teleport Scroll": teleport_user,
    "Sword": None
}
