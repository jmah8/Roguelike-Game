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

    def __init__(self, game_surface):
        self.x = game_surface.get_width() - (SPRITE_SIZE * ((TILE_WIDTH // 2) + (NUM_OF_BUTTONS // 2)))
        self.y = game_surface.get_height() - SPRITE_SIZE
        self.button_surface = pygame.Surface(((SPRITE_SIZE * NUM_OF_BUTTONS), SPRITE_SIZE))
        self.button_list = []
        self.button_count = 0

    def add_button(self, img, menu_option=None):
        print(self.x)
        button = Button(self.button_count, img, menu_option)
        self.button_list.append(button)
        self.button_count += 1

    def draw_buttons(self, game_surface):
        # Makes button_surface transparent
        self.button_surface.set_colorkey(BLACK)
        for button in self.button_list:
            self.button_surface.blit(button.image, button.rect)
        game_surface.blit(self.button_surface,
                          (self.x, self.y))

    def check_if_button_pressed(self, mouse_x, mouse_y):
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        for button in self.button_list:
            if button.rect.collidepoint(final_x, final_y):
                return button.menu_open
        return None
