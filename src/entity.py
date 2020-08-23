from constant import *
import config

class Entity:
    """
    Class for Entity which represents entity, which is anything that appears
    and acts in the game

    Attributes:
        game (arg, game): Game with all game data
        x (arg, int): Position on x axis
        y (arg, int): Position on y axis
        object_id (arg, string): id of Entity
        image_key (arg, string): key of sprite image
        anim_length (arg, int): number of sprites in animation

        left (bool): if Entity is facing left
        right (bool): if Entity is facing right
        moving (bool): if Entity is moving

        flicker_speed (float): how much time we spend on single frame
        flicker_timer (float): how much timer has passed
        anim_frame (int): current frame of animation

        creature (arg, Creature): Creature it is
        ai (arg, ai): Ai Entity has
        item (arg, Item): Item self is
        container (arg, Container): Container self is
    """

    def __init__(self, game, x, y, object_id, creature=None, ai=None, item=None, container=None, image_key=None):
        self.game = game
        self.x = x
        self.y = y
        self.object_id = object_id
        self.image_key = image_key

        if isinstance(config.SPRITE.sprite_dict[self.image_key], dict):
            self.anim_length = len(config.SPRITE.sprite_dict[self.image_key]["idle_right"])
        else:
            self.anim_length = 1

        self.left = False
        self.right = True
        self.moving = False

        if self.anim_length > 1:
            self.flicker_speed = ANIMATION_SPEED / self.anim_length / 1.0
            self.flicker_timer = 0.0
            self.anim_frame = 0

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

        self.item = item
        if item:
            item.owner = self

        self.container = container
        if container:
            container.owner = self

    @property
    def position(self):
        """
        Returns object's position

        Returns:
            Object's position
        """
        return self.x, self.y

    @property
    def rect(self):
        """
        Returns entity's rect position, ie where the entity is on the screen,
        which is different then self.x, self.y which is the position of entity
        in game

        Returns:
            Entity's rect position
        """
        return self.x * SPRITE_SIZE, self.y * SPRITE_SIZE

    @property
    def size(self):
        """
        Returns:
            Entity's sprite size, which is usually SPRITE_SIZE
        """
        return SPRITE_SIZE, SPRITE_SIZE

    @property
    def image(self):
        """
        Returns image that entity should show entity

        Returns:
            image (Sprite): Sprite that self should show
        """
        image = None
        if self.anim_length == 1:
            image = config.SPRITE.sprite_dict[self.image_key]
        else:
            if self.right:
                if self.moving:
                    image = config.SPRITE.sprite_dict[self.image_key]["run_right"][self.anim_frame]
                else:
                    image = config.SPRITE.sprite_dict[self.image_key]["idle_right"][self.anim_frame]
            else:
                if self.moving:
                    image = config.SPRITE.sprite_dict[self.image_key]["run_left"][self.anim_frame]
                else:
                    image = config.SPRITE.sprite_dict[self.image_key]["idle_left"][self.anim_frame]
        return image

    def update_anim(self):
        """
        Updates objects sprite depending on time passed
        and if it is moving and direction it is facing
        """
        if self.anim_length > 1:
            clock = config.CLOCK.get_fps()

            if clock > 0.0:
                self.flicker_timer += 1 / clock

            if self.flicker_timer >= self.flicker_speed:
                self.flicker_timer = 0.0

                self.anim_frame += 1
                self.anim_frame %= self.anim_length
                self.moving = False

    def update(self, dx, dy):
        """
        Updates the Entity depending on its ai or player input
        """
        if self.ai:
            self.ai.take_turn()
        else:
            self.creature.move(dx, dy)

        if self.creature.stat:
            # Regenerates hp and mp of creatures
            self.creature.regen(self.game.turn_count)


