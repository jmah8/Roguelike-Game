from constant import *

class Entity(pygame.sprite.Sprite):
    """
    Class for Entity which represents entity, which is anything that appears
    and acts in the game

    Attributes:
        game (arg, game): Game with all game data
        x (arg, int): Position on x axis
        y (arg, int): Position on y axis
        object_id (arg, string): id of Entity
        image (arg, sprite): Sprite of image
        anim (arg, [string][int]): dictionary of sprites for animation
        creature (arg, Creature): Creature it is
        ai (arg, ai): Ai Entity has
        item (arg, Item): Item self is
        container (arg, Container): Container self is
        flicker_speed (float): how much time we spend on single frame
        flicker_timer (float): how much timer has passed
        anim_frame (int): current frame of animation
    """

    def __init__(self, game, x, y, object_id, image=None, anim=None, creature=None, ai=None, item=None, container=None):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.x = x
        self.y = y
        self.object_id = object_id
        self.anim = anim
        self.image = image

        if not self.image:
            self.image = anim['idle_right'][0]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x * SPRITE_SIZE, self.y * SPRITE_SIZE)

        self.left = False
        self.right = True
        self.moving = False

        if (anim):
            self.flicker_speed = ANIMATION_SPEED / len(self.anim) / 1.0
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

    def update_anim(self):
        """
        Updates objects sprite depending on time passed
        and if it is moving and direction it is facing
        """
        if self.anim:
            clock = self.game.clock.get_fps()

            if clock > 0.0:
                self.flicker_timer += 1 / clock

            if self.flicker_timer >= self.flicker_speed:
                self.flicker_timer = 0.0

                self.anim_frame += 1
                self.anim_frame %= len(self.anim)
                self.moving = False

            if self.right:
                if self.moving:
                    self.image = self.anim["run_right"][self.anim_frame]
                else:
                    self.image = self.anim["idle_right"][self.anim_frame]
            else:
                if self.moving:
                    self.image = self.anim["run_left"][self.anim_frame]
                else:
                    self.image = self.anim["idle_left"][self.anim_frame]

    def update(self, dx, dy):
        """
        Updates the Entity depending on its ai or player input
        """
        if self.ai:
            self.ai.take_turn()
        else:
            self.creature.move(dx, dy)

        # Regenerates hp and mp of creatures
        if self.game.turn_count % REGEN_TIME == 0:
            if self.creature.stat.hp + 1 < self.creature.stat.max_hp:
                self.creature.stat.hp += 1
            if self.creature.stat.max_mp + 1 < self.creature.stat.max_mp:
                self.creature.stat.mp += 1

