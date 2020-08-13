from constant import *


def text_height_helper(font):
    """
    Helper to retrieve height of font rect
    """
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()
    return font_rect.height


def messages_to_draw(game):
    """
    Store most recent NUM_MESSAGES in GAME_MESSAGES in to_draw
    """
    if len(game.GAME_MESSAGES) <= NUM_MESSAGES:
        to_draw = game.GAME_MESSAGES
    else:
        to_draw = game.GAME_MESSAGES[-NUM_MESSAGES:]
    return to_draw


def draw_text(display_surface, coord, text_color, text, text_bg_color=None):
    """
    displays text at coord on given surface

    Args:
        display_surface (surface): surface to draw to
        coord ((int, int)): coord to draw to
        text_color (color): color of text
        text (string): text to draw
        text_bg_color (color): background color of text
    """
    text_surface, text_rect = _text_to_objects_helper(
        text, text_color, text_bg_color)

    text_rect.topleft = coord

    display_surface.blit(text_surface, text_rect)


def _text_to_objects_helper(inc_text, inc_color, inc_bg_color):
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
