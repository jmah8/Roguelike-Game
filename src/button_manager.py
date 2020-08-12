from constant import *
import pygame
from exceptions import *


class Button:
    """
    Button class

    Attributes:
        image (arg, image): image of button
        rect (arg, rect): rect of image
        menu_open (arg, function): function to call when button clicked
    """
    def __init__(self, x, image, menu_open):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (SPRITE_SIZE * x, 0)
        self.menu_open = menu_open


class Button_Manager:
    """
    Manager for the bottom button panel for game

    Attributes:
        x (int): x position of button manager
        y (int): y position of button
        button_surface (surface): surface that holds the buttons.
            This surface is blitted to game surface
        button_dict (list): list of buttons
        button_count (int): number of buttons currently in button manager
        button_surface (arg, surface): surface that will hold all the buttons.
            Used for finding width and height of surface
    """

    def __init__(self, game_surface):
        self.x = game_surface.get_width() - (SPRITE_SIZE * ((TILE_WIDTH // 2) + (NUM_OF_BUTTONS // 2)))
        self.y = game_surface.get_height() - SPRITE_SIZE
        self.button_surface = pygame.Surface(((SPRITE_SIZE * NUM_OF_BUTTONS), SPRITE_SIZE))
        self.button_surface.set_colorkey(BLACK)
        self.button_dict = {}
        self.button_count = 0

    def add_button(self, img, button_id, menu_option=None):
        """
        Adds button to button manager

        Makes button and adds that button to button_list
        and increment button counter by 1

        Args:
            img (sprite): image of button
            button_id (string): the type of button it is. String must be
                unique
            menu_option (function): function to call when button pressed
        """
        if not self.button_count >= NUM_OF_BUTTONS:
            button = Button(self.button_count, img, menu_option)
            if button_id not in self.button_dict:
                self.button_dict[button_id] = button
                self.button_count += 1
            else:
                raise ButtonExistException("Button exist")

    def draw_buttons(self, game_surface):
        """
        Draws buttons onto param game_surface

        First draws buttons onto button_surface and then draws
        button_surface onto game_surface at self.x, self.y

        Args:
            game_surface (surface): surface to draw buttons on

        Returns:

        """
        for button in self.button_dict.values():
            self.button_surface.blit(button.image, button.rect)
        game_surface.blit(self.button_surface,
                          (self.x, self.y))

    def check_if_button_pressed(self, mouse_x, mouse_y):
        """
        Checks if any of the bottoms are clicked and returns
        button pressed if any, else return None

        Since the mouse_x, mouse_y is relative to topleft corner
        of screen but the first button's topleft is (0, 0), need to
        adjust mouse_x and mouse_y so that both are in sync

        Args:
            mouse_x (int): x position of mouse
            mouse_y (int): y position of mouse

        Returns:
            button (Button): button pressed
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        for button in self.button_dict.values():
            if button.rect.collidepoint(final_x, final_y):
                return button
        return None

    def check_if_specific_button_pressed(self, button_id, mouse_x, mouse_y):
        """
        Checks if button with button_id is clicked and returns
        button pressed if any, else return None

        Since the mouse_x, mouse_y is relative to topleft corner
        of screen but the first button's topleft is (0, 0), need to
        adjust mouse_x and mouse_y so that both are in sync

        Args:
            button_id (string): button_id of button to check
            mouse_x (int): x position of mouse
            mouse_y (int): y position of mouse

        Returns:
            button (Button): button pressed
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        button = self.button_dict[button_id]
        if button.rect.collidepoint(final_x, final_y):
            return button
        return None
