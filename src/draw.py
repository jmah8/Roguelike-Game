import game_text
import minimap
from constant import *
import fov
import sprite
from button_manager import Button_Manager


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
        for tile in self.game.all_tile:
            self.game_surface.blit(tile.image, self.game.camera.apply(tile))

        # Draws object if it is in player fov
        for obj in self.game.GAME_OBJECTS:
            if fov.check_if_in_fov(self.game, obj):
                obj.update_anim()
                self.game_surface.blit(obj.image, self.game.camera.apply(obj))

        # Draw mouse select cursor depending on if free camera is on
        if self.game.free_camera_on:
            self.game_surface.blit(self.game.free_camera.image, self.game.camera.apply(self.game.free_camera))
        else:
            self.draw_mouse()

        self.game.particles.draw(self.game_surface)
        self.game.particles.update()

        self.button_manager.draw_buttons(self.game_surface)

        self.draw_grid()

        if self.game.mini_map_on:
            self.draw_minimap(self.game)

        self.draw_debug()
        self.draw_messages()

    def add_buttons(self):
        """
        Adds clickable buttons to bottom of screen
        """
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
        to_draw = game_text.messages_to_draw(self.game)
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

    def draw_map(self):
        """
        Draws map. This map
        is a replica of the actual map
        """
        map_data = self.game.map_data
        tile_array = self.game.tile_array

        scale_tile_width = RESOLUTION[0] / map_data.map_width
        scale_tile_height = RESOLUTION[1] / map_data.map_height
        scale_factor_x = SPRITE_SIZE / scale_tile_width
        scale_factor_y = SPRITE_SIZE / scale_tile_height

        minimap = pygame.Surface((RESOLUTION[0], RESOLUTION[1]))

        for y in range(map_data.map_height):
            for x in range(map_data.map_width):
                tile = tile_array[y][x]
                tile_img, tile_img_rect = sprite.scale_for_minimap(tile, scale_factor_x, scale_factor_y)
                minimap.blit(tile_img, tile_img_rect)

        player_img, player_img_rect = sprite.scale_for_minimap(self.game.player, scale_factor_x, scale_factor_y)

        minimap.blit(player_img, player_img_rect)

        self.game_surface.blit(minimap, (0, 0))

    def draw_mouse(self):
        """
        Draws mouse_select image at mouse position

        Returns:

        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x // SPRITE_SIZE
        mouse_y = mouse_y // SPRITE_SIZE

        self.draw_img_at_coord(self.game.game_sprites.mouse_select, mouse_x, mouse_y)

    def draw_img_at_coord(self, img, x_coord, y_coord):
        """
        Draws img at (x_coord, y_coord)

        x and y _coord are coords on the map

        Args:
            img (sprite): image to draw at (x, y)
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
            relative_x, relative_y = self.game.get_relative_screen_coord(x, y, self.game.map_data, self.game.camera)
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
