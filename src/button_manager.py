from constant import *
import pygame


class Button:
    def __init__(self, x, image, menu_open):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (SPRITE_SIZE * x, 0)
        self.menu_open = menu_open

class Button_Manager:
    """
    Manager for the bottom button panel for game

    Attributes:
        button_surface (surface): surface that holds all the buttons.
            This surface is to be drawn to game
    """
    def __init__(self):
        self.button_surface = pygame.Surface(((SPRITE_SIZE * 6), SPRITE_SIZE))
        self.button_list = []
        self.button_count = 0

    def add_button(self, img, menu_option=None):
        button = Button(self.button_count, img, menu_option)
        self.button_list.append(button)
        self.button_count += 1

    def draw_buttons(self, game_surface):
        # Makes button_surface transparent
        self.button_surface.set_colorkey(BLACK)
        for b in self.button_list:
            self.button_surface.blit(b.image, b.rect)
        game_surface.blit(self.button_surface,
                          (0, 0))


    # def button(self, img, coords, game_surface):
    #     self.button_surface.blit(img, coords)
    #     # Makes button_surface transparent
    #     self.button_surface.set_colorkey(BLACK)
    #     button_rect = img.get_rect()
    #     button_rect.topright = coords
    #
    #     # TODO: blit button on surface with an offset to align multiple buttons
    #     game_surface.blit(self.button_surface,
    #                       (game_surface.get_width() - SPRITE_SIZE, game_surface.get_height() - SPRITE_SIZE))
    #     return (img, button_rect)
