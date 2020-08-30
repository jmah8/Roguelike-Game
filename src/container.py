class Container:
    def __init__(self, volume=10.0, inventory=[], equipped=None):
        self.inventory = inventory
        self.volume = volume
        self.equipped = equipped

    @property
    def equipped_items(self):
        equipped_item_list = [entity for entity in self.inventory
                              if entity.equipment and entity.equipment.equipped]

        return equipped_item_list

    ## TODO Get Name Inventory()
    ## TODO Get volume of container()
    ## TODO get weight of inventory()