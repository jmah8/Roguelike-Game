import gamemap
import pygame
from constant import *
import fov
import sprite
from button_manager import Button_Manager

class Drawing:
    def __init__(self, game):
        self.game = game
        self.button_manager = Button_Manager()

    def draw(self):
        """
        Draws map and entities
        """
        # Update what to lock camera on
        if (not self.game.free_camera_on):
            self.game.camera.update(self.game.player)
        else:
            self.game.camera.update(self.game.free_camera)

        if (not self.game.wall_hack):
            self.game.fov = fov.new_fov(self.game)
        fov.ray_casting(self.game, self.game.map_array, self.game.fov)
        fov.draw_seen(self.game, self.game.tile_array, self.game.fov)

        # Draws all tiles
        for tile in self.game.all_tile:
            self.game.surface.blit(tile.image, self.game.camera.apply(tile))

        if (self.game.free_camera_on):
            self.game.surface.blit(self.game.free_camera.image, self.game.camera.apply(self.game.free_camera))

        # Draws object if it is in player fov
        for obj in self.game.GAME_OBJECTS:
            if fov.check_if_in_fov(self.game, obj):
                obj.update_anim()
                self.game.surface.blit(obj.image, self.game.camera.apply(obj))

        self.draw_buttons()
        self.draw_grid()

        if (self.game.mini_map_on):
            self.draw_minimap(self.game)

        self.draw_debug()
        self.draw_messages()
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, self.game.camera.camera_width, SPRITE_SIZE):
            pygame.draw.line(self.game.surface, GREY, (x, 0), (x, self.game.camera.camera_height))

        for y in range(0, self.game.camera.camera_height, SPRITE_SIZE):
            pygame.draw.line(self.game.surface, GREY, (0, y), (self.game.camera.camera_width, y))

    def draw_debug(self):
        """
        Draws FPS counter on top right of screen
        """
        self.draw_text(self.game.surface, (self.game.camera.camera_width - 125, 15), WHITE,
                       "FPS: " + str(int(self.game.clock.get_fps())), BLACK)

    def draw_text(self, display_surface, coord, text_color, text, text_bg_color=None):
        """
        displays text at coord on given surface

        Args:
            display_surface (surface): surface to draw to
            coord ((int, int)): coord to draw to
            text_color (color): color of text
            text (string): text to draw
            text_bg_color (color): background color of text
        """
        text_surface, text_rect = self._text_to_objects_helper(
            text, text_color, text_bg_color)

        text_rect.topleft = coord

        display_surface.blit(text_surface, text_rect)

    def _text_to_objects_helper(self, inc_text, inc_color, inc_bg_color):
        """
        Helper function for draw_text. Returns the text surface and rect

        Args:
            inc_text (string): text to draw
            inc_color (color): color of text
            inc_bg_color (color): background color of text
        """
        if inc_bg_color:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color, inc_bg_color)
        else:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color, )
        return text_surface, text_surface.get_rect()

    def draw_messages(self):
        to_draw = self._messages_to_draw()
        text_height = self._text_height_helper(FONT_MESSAGE_TEXT)
        y_pos = self.game.camera.camera_height - (NUM_MESSAGES * text_height) - TEXT_SPACE_BUFFER
        messages_drawn_counter = 0
        for message, color in to_draw:
            self.draw_text(self.game.surface, (TEXT_SPACE_BUFFER,
                                               (y_pos + messages_drawn_counter * text_height)), color, message, None)
            messages_drawn_counter += 1

    """
    Helper to retrieve height of font rect
    """

    def _text_height_helper(self, font):
        font_object = font.render('a', False, (0, 0, 0))
        font_rect = font_object.get_rect()
        return font_rect.height

    """
    Store most recent NUM_MESSAGES in GAME_MESSAGES in to_draw
    """

    def _messages_to_draw(self):
        if len(self.game.GAME_MESSAGES) <= NUM_MESSAGES:
            to_draw = self.game.GAME_MESSAGES
        else:
            to_draw = self.game.GAME_MESSAGES[-NUM_MESSAGES:]
        return to_draw

    def print_game_message(self, ingame_message, message_color):
        self.game.GAME_MESSAGES.append((ingame_message, message_color))

    def draw_minimap_copy_map(self):
        """
        Draws minimap on topleft of screen. This minimap
        is a replica of the actual map
        """
        map_data = self.game.map_data
        tile_array = self.game.tile_array

        resol = max(RESOLUTION[0] // MINIMAP_SCALE, RESOLUTION[1] // MINIMAP_SCALE)
        scale_factor_x = (map_data.width // resol)
        scale_factor_y = (map_data.height // resol)


        # Code below displays:
        # Minimap is shrunk down version of actual map and
        # so shows players, enemies and items
        minimap = pygame.Surface((resol, resol))
        # map_data = self.game.map_data
        # scaled_map = pygame.transform.scale(self.game.surface,
        #     (MINIMAP_RESOLUTION))
        # minimap.blit(scaled_map, (0, 0))

        # Draws only map with fov but bad performance
        for y in range(map_data.tileheight):
            for x in range(map_data.tilewidth):
                tile = tile_array[y][x]
                tile_img, tile_img_rect = sprite.scale_for_minimap(tile, scale_factor_x, scale_factor_y)
                minimap.blit(tile_img, tile_img_rect)

        player_img, player_img_rect = sprite.scale_for_minimap(self.game.player, scale_factor_x, scale_factor_y)

        minimap.blit(player_img, player_img_rect)

        self.game.surface.blit(minimap, (0, 0))

    def draw_minimap(self, game):
        """
        Draws minimap on topleft of screen. This is a
        representation of the actual map

        Arg:
            game (Game): game to load minimap to
        """
        map_data = game.map_data

        resol = max(RESOLUTION[0] // MINIMAP_SCALE, RESOLUTION[1] // MINIMAP_SCALE)
        scale_factor_x = (map_data.width // resol)
        scale_factor_y = (map_data.height // resol)

        self._draw_minimap_walls(game, scale_factor_x, scale_factor_y)
        self._draw_minimap_rooms(game, scale_factor_x, scale_factor_y)
        self._draw_unseen_tile(game, scale_factor_x, scale_factor_y)
        self._draw_minimap_player(game, scale_factor_x, scale_factor_y)

    def _draw_minimap_player(self, game, scale_factor_x, scale_factor_y):
        """
        Draws player onto minimap

        Args:
            game (Game): Game to draw player on
            scale_factor_x (int): what to scale x by
            scale_factor_y (int): what to sclae y by
        """
        pygame.draw.rect(game.surface, RED,
                         ((game.player.rect.topleft[0] // scale_factor_x),
                          (game.player.rect.topleft[1] // scale_factor_y),
                          # + 1 is to make player directly touch walls
                          # without making too big of difference in size
                          (game.player.rect.size[0] // scale_factor_x + 1),
                          (game.player.rect.size[1] // scale_factor_y + 1)))

    def _draw_unseen_tile(self, game, scale_factor_x, scale_factor_y):
        """
        Draws unseen tiles

        Args:
            game (Game): Game to draw unseen tile on
            scale_factor_x (int): what to scale x by
            scale_factor_y (int): what to sclae y by
        """
        for y in range(game.map_data.tileheight):
            for x in range(game.map_data.tilewidth):
                tile = game.tile_array[y][x]
                if (isinstance(tile, gamemap.Floor) and not tile.seen):
                    pygame.draw.rect(game.surface, BLACK,
                                    ((tile.rect.topleft[0] // scale_factor_x),
                                    (tile.rect.topleft[1] // scale_factor_y),
                                     # + 2 is to make black cover everything since
                                     # add +1 twice for player and room
                                    (tile.rect.size[0] // scale_factor_x + 2),
                                    (tile.rect.size[1] // scale_factor_y + 2)))

    def _draw_minimap_rooms(self, game, scale_factor_x, scale_factor_y):
        """
        Draws rooms (and paths since paths are considered rooms)
        onto minimap

        Args:
            game (Game): Game to draw rooms on
            scale_factor_x (int): what to scale x by
            scale_factor_y (int): what to sclae y by
        """
        list_of_rooms = game.map_tree.root.child_room_list
        for room in list_of_rooms:
            pygame.draw.rect(game.surface, WHITE,
                             ((room.x * SPRITE_SIZE // scale_factor_x),
                              (room.y * SPRITE_SIZE // scale_factor_y),
                              # + 1 is to make paths directly touch room
                              # without making too big of difference in size
                              (room.width * SPRITE_SIZE // scale_factor_x + 1),
                              (room.height * SPRITE_SIZE // scale_factor_y + 1)))

    def _draw_minimap_walls(self, game, scale_factor_x, scale_factor_y):
        """
        Draws wall onto minimap

        Args:
            game (Game): Game to draw wall on
            scale_factor_x (int): what to scale x by
            scale_factor_y (int): what to sclae y by
        """
        pygame.draw.rect(game.surface, BLACK,
                         (0, 0,
                          game.map_data.width // scale_factor_x,
                          game.map_data.height // scale_factor_y))

    def button(self, img, coords, game_surface):
        self.button_surface.blit(img, coords)
        # Makes button_surface transparent
        self.button_surface.set_colorkey(BLACK)
        button_rect = img.get_rect()
        button_rect.topright = coords
        game_surface.blit(self.button_surface,
                          (game_surface.get_width() - SPRITE_SIZE, game_surface.get_height() - SPRITE_SIZE))
        return (img, button_rect)

    def draw_buttons(self):
        # InventoryButton
        self.button_manager.button(self.game.game_sprites.inventory_button, (0, 0), self.game.surface)

