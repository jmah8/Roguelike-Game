from constant import *


class Camera:
    """
    Camera that "follows" player around

    Camera is actually the whole map that gets offset whenever
    player moves and it offsets everything else relative to
    the camera's offset

    Attributes:
        map_width (arg, int): width of whole map
        map_height (arg, int): height of whole map
        camera_width (int): width of camera
        camera_height (int): height of camera
        map_width_tile (int): width of whole map in tiles
        map_height_tile (int): height of while map in tiles
    """

    def __init__(self, map_width, map_height, camera_width=CAMERA_WIDTH, camera_height=CAMERA_HEIGHT):
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

        self.camera_width = camera_width
        self.camera_height = camera_height

        self.map_width_tile = self.map_width // SPRITE_SIZE
        self.map_height_tile = self.map_height // SPRITE_SIZE

    def apply(self, entity):
        """
        Apply camera offset to entity 

        Args:
            entity (object): object to apply offset to
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, player):
        """
        Update the camera based on player position

        Args:
            player (object): player to follow
        """
        x = -player.rect.x + int(self.camera_width / 2)
        y = -player.rect.y + int(self.camera_height / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.map_width - self.camera_width), x)
        y = max(-(self.map_height - self.camera_height), y)
        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)

    @property
    def camera_position(self):
        """
        Returns the camera coords

        Returns:
            x (int): x coord of camera
            y (int): y coord of camera
        """
        x, y = self.camera.topleft
        return -x, -y

    def get_relative_screen_coord(self, x, y):
        """
        Returns the coord of (x_coord, y_coord) relative to the camera/screen

        Used for drawing images where calling apply is not possible
        since drawing at x = 15, y = 15 will draw it off the screen
        depending on screen size since apply is called to everything

        Args:
            x (int): x coord to translate
            y (int): y coord to translate

        Returns:
            relative_x, relative_y ((int, int)): Coordinate of (x_coord, y_coord) on screen
        """
        # Add camera position to get the mouse's map coordinate
        camera_x, camera_y = self.camera_position
        relative_x = x - (camera_x // SPRITE_SIZE)
        relative_y = y - (camera_y // SPRITE_SIZE)
        # Find the amount of tiles on screen
        screen_x = self.camera_width // SPRITE_SIZE
        screen_y = self.camera_height // SPRITE_SIZE

        # If map is smaller than screen x/y, this fixes the issue of
        # the mouse coord and map coord not being in sync

        # If map is smaller than screen, than subtract it by # of tiles not in map
        if self.map_width_tile < screen_x:
            relative_x = relative_x - (screen_x - self.map_width_tile)
        if self.map_height_tile < screen_y:
            relative_y = relative_y - (screen_y - self.map_height_tile)

        return relative_x, relative_y

    def get_mouse_coord(self):
        """
        Returns mouse coordinate on map, taking into account
        size of map

        First converts the mouse position to coordinate. Since mouse
        position is found relative to screen, add to it the camera position
        to get the mouse's map coordinate.

        Returns:
            mouse_x, mouse_y ((int, int)): Coordinate of mouse on map
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Converts the mouse position to coordinate (relative to screen)
        mouse_x = mouse_x // SPRITE_SIZE
        mouse_y = mouse_y // SPRITE_SIZE
        # Add camera position to get the mouse's map coordinate
        x, y = self.camera_position
        mouse_x = mouse_x + (x // SPRITE_SIZE)
        mouse_y = mouse_y + (y // SPRITE_SIZE)
        # Find the amount of tiles on screen
        screen_x = self.camera_width // SPRITE_SIZE
        screen_y = self.camera_height // SPRITE_SIZE

        # If map is smaller than screen x/y, this fixes the issue of
        # the mouse coord and map coord not being in sync

        # If map is smaller than screen, than subtract it by # of tiles not in map
        if self.map_width_tile < screen_x:
            mouse_x = mouse_x - (screen_x - self.map_width_tile)
        if self.map_height_tile < screen_y:
            mouse_y = mouse_y - (screen_y - self.map_height_tile)

        return mouse_x, mouse_y
