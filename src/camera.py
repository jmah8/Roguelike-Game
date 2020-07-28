from constant import *

class Camera:
    """
    Camera that "follows" player around

    Camera is actually the whole map that gets offset whenever
    player moves and it offsets everything else relative to
    the camera's offset

    Args:
        width (int): width of whole map
        height (int): height of whole map
        camera (rect): rect of whole map
    """
    def __init__(self, width, height, camera_width=CAMERA_WIDTH, camera_height=CAMERA_HEIGHT):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.camera_width = camera_width
        self.camera_height = camera_height

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
        x = max(-(self.width - self.camera_width), x)
        y = max(-(self.height - self.camera_height), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


def find_object_offset(object, map_data):
    """
    Find where to draw the camera relative to the object

    Args:
        object (object): player to find where to
            draw camera relative to
        map_data (MapInfo): data of map
    """
    rect = object.rect 
    x = -rect.x + int(CAMERA_WIDTH / 2)
    y = -rect.y + int(CAMERA_HEIGHT / 2)

    x = min(0, x)
    y = min(0, y)
    x = max(-(map_data.width - CAMERA_WIDTH), x)
    y = max(-(map_data.height - CAMERA_HEIGHT), y)
    return -x,-y