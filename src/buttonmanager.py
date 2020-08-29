from exceptions import *
from constant import *
import config
import menu
import game


class IconButton:
    """
    IconButton class

    Args:
        x (int): x coord of button

    Attributes:
        image (arg, image): image of button
        rect (arg, rect): rect of image
        menu_open_fn (arg, function): function to call when button clicked
        mouse_over_fn (arg, function): Function to call when button is hovered over
    """
    def __init__(self, x, y, image, menu_open_fn=None, mouse_over_fn=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (SPRITE_SIZE * x, SPRITE_SIZE * y)
        self.menu_open_fn = menu_open_fn
        self.mouse_over_fn = mouse_over_fn

    def check_if_button_hovered(self, x, y):
        """
        Return if button is hovered over

        Args:
            x (int): x coord of mouse
            y (int): y coord of mouse

        Returns:
            mouse_over (int): True if button is hovered over else false
        """
        mouse_over = (self.rect.left <= x <= self.rect.right and
                      self.rect.top <= y <= self.rect.bottom)
        return mouse_over

    def check_if_button_clicked(self, x, y):
        """
        Return if button pressed

        Args:
            x (int): x coord of mouse
            y (int): y coord of mouse

        Returns:
            True if button is clicked else false
        """
        if self.rect.collidepoint(x, y):
            return True
        return False


class ButtonManager:
    """
    Manager for the bottom button panel for game

    Attributes:
        num_button (arg, int): max number of buttons
        x (int): x position of button manager
        y (int): y position of button
        width (int): width of button manager in icons
        height (int): height of button manager in icons
        button_surface (surface): surface that holds the buttons.
            This surface is blitted to game surface
        button_dict (list): list of buttons
        button_count (int): number of buttons currently in button manager
    """

    def __init__(self, x, y, width, height, num_button):
        self.num_button = num_button
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_surface = pygame.Surface(((SPRITE_SIZE * self.width), (SPRITE_SIZE * self.height)))
        self.button_surface.set_colorkey(BLACK)
        self.button_dict = {}
        self.button_count = 0

    def add_button(self, icon_button, button_id):
        """
        Adds created IconButton

        Raises IconButtonException when button_id
        is already in button_dict

        Args:
            icon_button (IconButton): IconButton to add
            button_id (String): String of button key
        """
        if not self.button_count >= self.num_button and button_id not in self.button_dict:
            self.button_dict[button_id] = icon_button
            self.button_count += 1
        else:
            raise IconButtonException("IconButton exist")

    def create_button(self, img, button_id, menu_option=None):
        """
        Creates IconButton and adds it to button manager

        Makes button and adds that button to button_list
        and increment button counter by 1

        Raises IconButtonException when button_id
        is already in button_dict

        Args:
            img (sprite): image of button
            button_id (string): the type of button it is. String must be
                unique
            menu_option (function): function to call when button pressed
        """
        if not self.button_count >= self.num_button:
            if button_id not in self.button_dict:
                # The x and y coord of button depends on
                # nums of button currently in ButtonManager
                x = self.button_count % self.width
                y = self.button_count // self.width
                button = IconButton(x, y, img, menu_option)
                self.button_dict[button_id] = button
                self.button_count += 1
            else:
                raise IconButtonException("IconButton exist")

    def remove_button(self, button_id):
        if button_id in self.button_dict:
            self.button_dict.pop(button_id)
            self.button_count -= 1
        else:
            raise IconButtonException("IconButton doesn't exist")

    def get_button(self, button_id):
        """
        Args:
            button_id (String): Key of button_id

        Returns:
            Returns button with key of button_id
        """
        return self.button_dict[button_id]

    def draw_buttons(self, surface):
        """
        Draws buttons

        First draws buttons onto button_surface and then draws
        button_surface onto config.SURFACE_MAIN at self.x, self.y

        Args:
            surface (Surface): Surface to draw buttons on

        Returns:

        """
        for key in self.button_dict:
            button = self.button_dict[key]
            self.button_surface.blit(button.image, button.rect)
        surface.blit(self.button_surface,
                          (self.x, self.y))

    def check_if_button_hovered(self, mouse_x, mouse_y):
        """
        Checks if any of the bottoms are hovered over and returns
        button hovered over if any, else return None

        Since the mouse_x, mouse_y is relative to topleft corner
        of screen but the first button's topleft is (0, 0), need to
        adjust mouse_x and mouse_y so that both are in sync

        Args:
            mouse_x (int): x position of mouse
            mouse_y (int): y position of mouse

        Returns:
            button (IconButton): button hovered over
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        for button in self.button_dict.values():
            if button.check_if_button_hovered(final_x, final_y):
                return button
        return None

    def check_if_specific_button_hovered(self, button_id, mouse_x, mouse_y):
        """
        Checks if button with button_id is hovered over and returns
        button hovered over if any, else return None

        Since the mouse_x, mouse_y is relative to topleft corner
        of screen but the first button's topleft is (0, 0), need to
        adjust mouse_x and mouse_y so that both are in sync

        Args:
            button_id (string): button_id of button to check
            mouse_x (int): x position of mouse
            mouse_y (int): y position of mouse

        Returns:
            button (IconButton): button hovered over
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        button = self.button_dict[button_id]
        if button.check_if_button_hovered(final_x, final_y):
            return button
        return None

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
            button (IconButton): button pressed
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        for button in self.button_dict.values():
            if button.check_if_button_clicked(final_x, final_y):
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
            button (IconButton): button pressed
        """
        final_x = mouse_x - self.x
        final_y = mouse_y - self.y
        button = self.button_dict[button_id]
        if button.check_if_button_clicked(final_x, final_y):
            return button
        return None


def add_buttons():
    """
    Adds clickable buttons to bottom of screen
    """
    config.BUTTON_PANEL.create_button(config.SPRITE.knight_anim[0], 'stats', menu.stat_menu)
    config.BUTTON_PANEL.create_button(config.SPRITE.inventory_button, 'inventory', menu.inventory_menu)
    config.BUTTON_PANEL.create_button(config.SPRITE.minimap_button, 'minimap', game.toggle_minimap)
    config.BUTTON_PANEL.create_button(config.SPRITE.minimap_button, 'map', menu.map_menu)