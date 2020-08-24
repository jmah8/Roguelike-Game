import collections
import config
import game
from constant import *


class GameData:
    def __init__(self):
        self.creature_data = {
            "player": [],
            "enemy": []
        }
        self.item_data = []
        self.game_messages = []
        self.previous_levels = collections.deque()
        self.next_levels = collections.deque()

    def transition_previous_level(self):
        """
        Go to previous level
        """
        if config.GAME_DATA.previous_levels:
            # Saves current level to next level list
            level_data = (
                config.PLAYER.x, config.PLAYER.y, config.MAP_INFO, config.GAME_DATA.creature_data["enemy"],
                config.GAME_DATA.item_data)
            config.GAME_DATA.next_levels.append(level_data)

            x, y, map_info, enemy_list, item_group = config.GAME_DATA.previous_levels.popleft()

            self._load_level_data(enemy_list, item_group, map_info, x, y)

    def transition_next_level(self):
        """
        Goes to next level
        """
        level_data = (
            config.PLAYER.x, config.PLAYER.y, config.MAP_INFO, config.GAME_DATA.creature_data["enemy"],
            config.GAME_DATA.item_data)
        config.GAME_DATA.previous_levels.append(level_data)

        if not config.GAME_DATA.next_levels:
            game.new()
            # Places upstair at where the player entered the map at
            config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type = UPSTAIR
        else:
            x, y, map_info, enemy_list, item_group = config.GAME_DATA.next_levels.popleft()

            self._load_level_data(enemy_list, item_group, map_info, x, y)

    def _load_level_data(self, enemy_list, item_group, map_info, x, y):
        """
        Loads level data to game variables

        Args:
            enemy_list (List): list of enemies on level
            item_group (List): list of items on level
            map_info (MapInfo): map info of level
            x (int): player's x position on level
            y (int): player's y position on level
        """
        config.PLAYER.x = x
        config.PLAYER.y = y
        config.GAME_DATA.creature_data["enemy"] = enemy_list
        config.GAME_DATA.item_data = item_group
        config.MAP_INFO = map_info
        game.generate_camera()
        game.initialize_pathfinding()

