import gamemap
import pygame
from constant import *
import fov
import sprite
import camera
from button_manager import Button_Manager

class Drawing:
    def __init__(self, game):
        self.game = game
        self.button_manager = Button_Manager()

    def draw(self):
        """
        Draws map and entities
        """
        if (not self.game.wall_hack):
            self.game.fov = fov.new_fov(self.game)
        fov.ray_casting(self.game, self.game.map_array, self.game.fov)
        fov.draw_seen(self.game, self.game.tile_array, self.game.fov)

        # Draws all tiles
        for tile in self.game.all_tile:
            self.game.map_surface.blit(tile.image, tile.rect)


        # Draws object if it is in player fov
        for obj in self.game.GAME_OBJECTS:
            if fov.check_if_in_fov(self.game, obj):
                obj.update_anim()
                self.game.map_surface.blit(obj.image, obj.rect)

        
        if (self.game.free_camera_on):
            self.game.map_surface.blit(self.game.free_camera.image, self.game.free_camera.rect)

        if (self.game.free_camera_on):
            x,y = camera.find_object_offset(self.game.free_camera, self.game.map_data)
        else:
            x,y = camera.find_object_offset(self.game.player, self.game.map_data)

        self.game.surface.blit(self.game.map_surface, (0, 0), (x, y, CAMERA_WIDTH, CAMERA_HEIGHT))
        
        self.draw_buttons()
        self.draw_grid()

        if (self.game.mini_map_on):
            self.draw_minimap_test()


        self.draw_debug()
        self.draw_messages()
        pygame.display.update()

    def draw_grid(self):
        for x in range(0, CAMERA_WIDTH, SPRITE_SIZE):
            pygame.draw.line(self.game.surface, GREY, (x, 0), (x, CAMERA_HEIGHT))

        for y in range(0, CAMERA_HEIGHT, SPRITE_SIZE):
            pygame.draw.line(self.game.surface, GREY, (0, y), (CAMERA_WIDTH, y))

    def draw_debug(self):
        """
        Draws FPS counter on top right of screen
        """
        self.draw_text(self.game.surface, (CAMERA_WIDTH - 125, 15), WHITE,
                       "FPS: " + str(int(self.game.clock.get_fps())), BLACK)

    def draw_text(self, display_surface, coord, text_color, text, text_bg_color=None):
        """
        displays text at coord on given surface

        Args:
            display_surface (surface, arg): surface to draw to
            coord ((int, int), arg): coord to draw to
            text_color (color, arg): color of text
            text (string, arg): text to draw
            text_bg_color (color, arg): background color of text
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
            inc_color (color, arg): color of text
            inc_bg_color (color, arg): background color of text
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
        y_pos = CAMERA_HEIGHT - (NUM_MESSAGES * text_height) - TEXT_SPACE_BUFFER
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

    def draw_minimap(self):
        """
        Draws minimap on topleft of screen
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
        # scaled_map = pygame.transform.scale(self.game.surface,
        #     (MINIMAP_RESOLUTION))
        # minimap.blit(scaled_map, (0, 0))

        # Draws only map with fov but bad performance
        for y in range (map_data.tileheight):
            for x in range (map_data.tilewidth):
                tile = tile_array[y][x]
                tile_img = pygame.transform.scale(tile.image,
                    (tile.rect.size[0] // scale_factor_x,
                    tile.rect.size[1] // scale_factor_y))
                tile_img_rect = tile_img.get_rect()
                tile_img_rect.topleft = (tile.rect.topleft[0] // scale_factor_x,
                                        tile.rect.topleft[1] // scale_factor_y)
                minimap.blit(tile_img, tile_img_rect)

        self.game.surface.blit(minimap, (0, 0))


    def draw_minimap_test(self):
        map_data = self.game.map_data

        resol = max(RESOLUTION[0] // MINIMAP_SCALE, RESOLUTION[1] // MINIMAP_SCALE)
        minimap = pygame.Surface((resol, resol))

        scale_factor_x = (map_data.width // resol)
        scale_factor_y = (map_data.height // resol)

        scaled_map = pygame.transform.scale(self.game.map_surface,
            (map_data.width // scale_factor_x, map_data.height // scale_factor_y))
        minimap.blit(scaled_map, (0, 0))

        self.game.surface.blit(minimap, (0, 0))

    def draw_buttons(self):
        # InventoryButton
        self.button_manager.button(self.game.game_sprites.inventory_button, (0, 0), self.game.surface)

