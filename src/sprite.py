from constant import *
import os


def load_image(name, colorkey=None, sprite_size=(SPRITE_SIZE, SPRITE_SIZE), convert_alpha=True):
    """
    Load and convert image to surface and returns image and the image rect
    and makes color at colorkey transparent

    Args:
        name (string) : Pathname of image to convert
        colorkey ((int, int)) : Position of color to be transparent
        sprite_size ((int, int)): Size of resulting image
        convert_alpha (bool): True if image already has transparent background,
            otherwise False with colorkey set to make transparent background
    """
    pathname = os.path.join(RESOURCE_PATH, name)
    try:
        image = pygame.image.load(pathname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(name)
    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    image = pygame.transform.scale(image, sprite_size)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image


def load_anim(pathname, start_num, end_num, convert_alpha=True):
    """
    Load list of sprites animations

    This function assumes that there is only one difference
    in filename for the animation sprites and that the difference
    is a number

    Args:
        pathname (string): image path name
        start_num (int): image file name start #
        end_num (int): image file name end #
    """
    sprite_anim = []
    sprite_anim.append(load_image(pathname, convert_alpha=convert_alpha))
    tmp = pathname
    for i in range(start_num, end_num):
        tmp = tmp.replace(str(i), str(i + 1))
        sprite_anim.append(load_image(tmp))
    return sprite_anim


def seen_sprite(image):
    """
    Converts an image, to a seen image

    Args:
        image (sprite): image to convert to seen image
    """
    seen_image = image.copy()
    seen_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
    return seen_image


def flip_anim(anim_array):
    """
    Flips animation image to face the other way

    Arg:
        anim_array (list): list of sprite's animation to flip
    """
    flip_anim = []
    for i in anim_array:
        flip_anim.append(pygame.transform.flip(i, True, False))
    return flip_anim


def scale_for_minimap(obj, scale_factor_x, scale_factor_y):
    """
    Scales obj image by scale_factor x and y

    Arg:
        obj (Entity): Entity with image to scale
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to scale y by
    """
    obj_img = pygame.transform.scale(obj.image,
                                     (int(obj.rect.size[0] / scale_factor_x),
                                      int(obj.rect.size[1] / scale_factor_y)))
    obj_img_rect = obj_img.get_rect()
    obj_img_rect.topleft = (int(obj.rect.topleft[0] / scale_factor_x),
                            int(obj.rect.topleft[1] // scale_factor_y))
    return obj_img, obj_img_rect


class GameSprites:
    """
    Class that holds all the sprite images
    """

    def __init__(self):
        #  Environment
        self.wall_image = load_image(WALL_1)
        self.seen_wall_image = seen_sprite(self.wall_image)

        self.floor_image_1 = load_image(FLOOR_1)
        self.seen_floor_image_1 = seen_sprite(self.floor_image_1)

        self.floor_image_2 = load_image(FLOOR_2)
        self.seen_floor_image_2 = seen_sprite(self.floor_image_2)

        self.upstair = load_image(STAIR_UP)
        self.seen_upstair = seen_sprite(self.upstair)

        self.downstair = load_image(STAIR_DOWN)
        self.seen_downstair = seen_sprite(self.downstair)

        self.unseen_tile = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.unseen_tile.fill(BLACK)

        self.select_tile = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.select_tile.fill(YELLOW)
        self.select_tile.set_alpha(75)


        # Creatures
        self.slime_anim = load_anim(SLIME, 0, 5)
        self.slime_run_anim = load_anim(SLIME_RUN, 0, 5)
        self.slime_dict = {
            "idle_right": self.slime_anim,
            "idle_left": flip_anim(self.slime_anim),
            "run_right": self.slime_run_anim,
            "run_left": flip_anim(self.slime_run_anim)
        }

        self.goblin_anim = load_anim(GOBLIN, 0, 5)
        self.goblin_run_anim = load_anim(GOBLIN_RUN, 0, 5)
        self.goblin_dict = {
            "idle_right": self.goblin_anim,
            "idle_left": flip_anim(self.goblin_anim),
            "run_right": self.goblin_run_anim,
            "run_left": flip_anim(self.goblin_run_anim)
        }

        self.skeleton_anim = load_anim(SKELETON, 0, 3)
        self.skeleton_run_anim = load_anim(SKELETON_RUN, 0, 3)
        self.skeleton_dict = {
            "idle_right": self.skeleton_anim,
            "idle_left": flip_anim(self.skeleton_anim),
            "run_right": self.skeleton_run_anim,
            "run_left": flip_anim(self.skeleton_run_anim)
        }

        # Knight
        self.knight_anim = load_anim(KNIGHT, 0, 5)
        self.knight_run_anim = load_anim(KNIGHT_RUN, 0, 5)
        self.knight_dict = {
            "idle_right": self.knight_anim,
            "idle_left": flip_anim(self.knight_anim),
            "run_right": self.knight_run_anim,
            "run_left": flip_anim(self.knight_run_anim)
        }

        # Items
        self.empty_inventory_slot = load_image(EMPTY_INVENTORY_SLOT)
        self.sword = load_image(SWORD, -1)

        # Consumables
        self.red_potion = load_image(RED_POTION)

        # UI
        self.inventory_button = load_image(INVENTORY)
        self.mouse_select = load_image(MOUSE_SELECT)
        self.equip_screen = load_image(EQUIP_SCREEN, None, (TILE_WIDTH // 2 * SPRITE_SIZE, TILE_HEIGHT // 2 * SPRITE_SIZE))
        self.minimap_button = load_image(MINIMAP_BUTTON)


        self.magic = {
            "fireball": load_image(FIREBALL),
            "lightning": load_image(LIGHTNING)
        }

        self.sprite_dict = {
            # Creatures
            "slime_dict": {
                "idle_right": self.slime_anim,
                "idle_left": flip_anim(self.slime_anim),
                "run_right": self.slime_run_anim,
                "run_left": flip_anim(self.slime_run_anim)
            },
            "goblin_dict": {
                "idle_right": self.goblin_anim,
                "idle_left": flip_anim(self.goblin_anim),
                "run_right": self.goblin_run_anim,
                "run_left": flip_anim(self.goblin_run_anim)
            },
            "skeleton_dict": {
                "idle_right": self.skeleton_anim,
                "idle_left": flip_anim(self.skeleton_anim),
                "run_right": self.skeleton_run_anim,
                "run_left": flip_anim(self.skeleton_run_anim)
            },
            # Knight
            "knight_dict": {
                "idle_right": self.knight_anim,
                "idle_left": flip_anim(self.knight_anim),
                "run_right": self.knight_run_anim,
                "run_left": flip_anim(self.knight_run_anim)
            },
            ""
            # Items
            "sword": self.sword,
            # Consumables
            "red_potion": self.red_potion,
            "mouse_select": self.mouse_select
        }