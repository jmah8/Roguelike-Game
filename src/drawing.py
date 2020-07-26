import gamemap
import pygame
from constant import *

class Drawing:
    def __init__(self, game):
        self.game = game

    def draw(self):
        """
        Draws map and entities
        """
        if (not self.game.wall_hack):
            self.game.fov = gamemap.new_fov(self.game)
        gamemap.ray_casting(self.game, self.game.map_array, self.game.fov)
        gamemap.draw_seen(self.game, self.game.tile_array, self.game.fov)

        # Draws all tiles
        for tile in self.game.all_tile:
            self.game.surface.blit(tile.image, self.game.camera.apply(tile))


        if (self.game.free_camera_on):
            self.game.surface.blit(self.game.free_camera.image, self.game.camera.apply(self.game.free_camera))

        # Draws object if it is in player fov
        for obj in self.game.GAME_OBJECTS:
            if gamemap.check_if_in_fov(self.game, obj):
                obj.update_anim()
                self.game.surface.blit(obj.image, self.game.camera.apply(obj))

        self.draw_grid()
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

        Arg:
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

        Arg:
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