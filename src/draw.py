import game_text
import minimap
from constant import *
import fov
import sprite
from button_manager import Button_Manager
import game


class Drawing:
    def __init__(self, game, game_surface):
        """
        Class that draws the game

        Attributes:
            game (arg, Game): Game with game data
            game_surface (arg, Surface): Surface to draw on
            button_manager (ButtonManager): Class that holds the bottom buttons
        """
        self.game = game
        self.game_surface = game_surface
        self.button_manager = Button_Manager(self.game_surface)

    def draw(self):
        """
        Draws map and entities

        Note: Always call game.clock.tick(FPS) before and pygame.display.flip()
        after calling this method to update display
        """
        # Draws all tiles
        self.draw_tiles()

        self.draw_game_objects()

        self.draw_grid()

        self.draw_particles()

        self.button_manager.draw_buttons()

        self.draw_ui()

        if self.game.mini_map_on:
            self.draw_minimap(self.game)

    def draw_ui(self):
        """
        Draws ui part of game
        """
        self.draw_player_stats(self.game.player)
        self.draw_debug()
        self.draw_messages()

    def draw_at_camera_offset_without_image(self, obj):
        """
        Draws obj on surface taking into account camera offset

        Args:
            obj (Object): Entity to draw
        """
        self.game_surface.blit(obj.image, self.game.camera.apply_without_image(obj))

    def draw_at_camera_offset_with_image(self, obj):
        """
        Draws obj on surface taking into account camera offset

        Args:
            obj (Object): Entity to draw
        """
        self.game_surface.blit(obj.image, self.game.camera.apply_with_image(obj))

    def draw_tiles(self):
        """
        Draws all tiles offset by camera
        """
        for col in self.game.map_info.tile_array:
            for tile in col:
                self.draw_at_camera_offset_without_image(tile)

    def draw_game_objects(self):
        """
        Draws all game objects offset by camera
        """
        self._draw_items()
        self._draw_creatures()

    def _draw_items(self):
        """
        Draws item if the tile item is on is seen offset by camera
        """
        for item in self.game.item_group:
            if self.game.map_info.tile_array[item.y][item.x].seen:
                self.draw_at_camera_offset_without_image(item)

    def _draw_creatures(self):
        """
        Draws all creatures in player FOV offset by camera
        """
        for creature in self.game.creature_data["enemy"] + self.game.creature_data["player"]:
            if fov.check_if_in_fov(self.game, creature):
                creature.update_anim()
                self.draw_at_camera_offset_without_image(creature)

    def draw_particles(self):
        """
        Draws all particles shifted by camera and updates them after
        """
        for particle in self.game.particles:
            self.draw_at_camera_offset_with_image(particle)
            particle.update()

    def add_buttons(self):
        """
        Adds clickable buttons to bottom of screen
        """
        self.button_manager.add_button(self.game.game_sprites.knight_anim[0], 'stats',
                                       self.game.menu_manager.stat_menu)
        self.button_manager.add_button(self.game.game_sprites.inventory_button, 'inventory',
                                       self.game.menu_manager.inventory_menu)
        self.button_manager.add_button(self.game.game_sprites.minimap_button, 'minimap', self.game.toggle_minimap)
        self.button_manager.add_button(self.game.game_sprites.minimap_button, 'map', self.game.menu_manager.map_menu)

    def draw_grid(self):
        for x in range(0, self.game.camera.camera_width, SPRITE_SIZE):
            pygame.draw.line(self.game_surface, GREY, (x, 0), (x, self.game.camera.camera_height))

        for y in range(0, self.game.camera.camera_height, SPRITE_SIZE):
            pygame.draw.line(self.game_surface, GREY, (0, y), (self.game.camera.camera_width, y))

    def draw_debug(self):
        """
        Draws FPS counter on top right of screen
        """
        game_text.draw_text(self.game_surface, (self.game.camera.camera_width - 125, 15), WHITE,
                       "FPS: " + str(int(self.game.clock.get_fps())), BLACK)

    def draw_messages(self):
        to_draw = game_text.messages_to_draw(self.game.GAME_MESSAGES)
        text_height = game_text.text_height_helper(FONT_MESSAGE_TEXT)
        y_pos = self.game.camera.camera_height - (NUM_MESSAGES * text_height) - TEXT_SPACE_BUFFER
        messages_drawn_counter = 0
        for message, color in to_draw:
            game_text.draw_text(self.game_surface, (TEXT_SPACE_BUFFER,
                                                    (y_pos + messages_drawn_counter * text_height)), color, message,
                                None)
            messages_drawn_counter += 1

    def add_game_message_to_print(self, ingame_message, message_color):
        """
        Adds game message to print

        Args:
            ingame_message (String): Message to add
            message_color (Color): Color of message
        """
        self.game.GAME_MESSAGES.append((ingame_message, message_color))

    def draw_map_menu(self):
        """
        Draws map. This map
        is a replica of the actual map
        """
        map_data = self.game.map_info
        tile_array = self.game.map_info.tile_array

        scale_tile_width = RESOLUTION[0] / map_data.tile_width
        scale_tile_height = RESOLUTION[1] / map_data.tile_height
        scale_factor_x = SPRITE_SIZE / scale_tile_width
        scale_factor_y = SPRITE_SIZE / scale_tile_height

        minimap = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))

        for y in range(map_data.tile_height):
            for x in range(map_data.tile_width):
                tile = tile_array[y][x]
                tile_img, tile_img_rect = sprite.scale_for_minimap(tile, scale_factor_x, scale_factor_y)
                minimap.blit(tile_img, tile_img_rect)

        player_img, player_img_rect = sprite.scale_for_minimap(self.game.player, scale_factor_x, scale_factor_y)

        minimap.blit(player_img, player_img_rect)

        self.game_surface.blit(minimap, (0, 0))

    def draw_mouse(self):
        """
        Draws mouse_select image at mouse position
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x // SPRITE_SIZE
        mouse_y = mouse_y // SPRITE_SIZE

        self.draw_img_at_coord(self.game.game_sprites.mouse_select, mouse_x, mouse_y)

    def draw_img_at_coord(self, img, x_coord, y_coord):
        """
        Draws img at (x_coord, y_coord) relative to screen

        x and y coord are coords on the map

        Args:
            img (sprite): image to update at (x, y)
            x_coord (int): x coord to draw tile onto
            y_coord (int): y coord to draw tile onto
        """
        self.game_surface.blit(img, (x_coord * SPRITE_SIZE, y_coord * SPRITE_SIZE))

    def draw_magic_path(self, line):
        """
        Highlights the path the spell will take

        Args:
            line (List): List of coords the spell will pass through
        """
        for (x, y) in line:
            relative_x, relative_y = self.game.camera.get_relative_screen_coord(x, y)
            self.draw_img_at_coord(self.game.game_sprites.select_tile, relative_x, relative_y)

    def draw_minimap(self, game):
        """
        Draws minimap on topleft of screen. This is a
        representation of the actual map.

        Args:
            game (Game): Game to load minimap to
        """
        if READ_FROM_FILE:
            minimap.draw_minimap_loaded_map(game)
        else:
            minimap.draw_minimap_generated_map(game)

    def draw_player_stats(self, player):
        hp = player.creature.stat.hp / player.creature.stat.max_hp
        mp = player.creature.stat.mp / player.creature.stat.max_mp
        exp = player.creature.stat.exp / 100
        pygame.draw.rect(self.game_surface, RED, (0, 0, HP_BAR_WIDTH * hp, HP_BAR_HEIGHT))
        pygame.draw.rect(self.game_surface, BLUE, (0, HP_BAR_HEIGHT, MP_BAR_WIDTH * mp, MP_BAR_HEIGHT))
        pygame.draw.rect(self.game_surface, YELLOW, (0, HP_BAR_HEIGHT+MP_BAR_HEIGHT, EXP_BAR_WIDTH * exp, EXP_BAR_HEIGHT))





