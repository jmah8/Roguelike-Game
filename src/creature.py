from particle import *


class Creature:
    """
    have hp
    can damage other objects
    can die

    Attributes:
        name_instance (arg, string) : Name of creature
        hp (arg, int) : HP of creature
        owner (object) : object that has self as creature component
        killable (arg, boolean) : if creature is killable
        enemy_group (arg, group): group creature can attack
        walk_through_tile (arg, boolean): if creature can walk through tiles like walls
        current_path (arg, List): List of path from start to goal
    """

    def __init__(self, name_instance, hp, killable=None, enemy_group=None, walk_through_tile=False, current_path=None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.owner = None
        self.killable = killable
        self.enemy_group = enemy_group
        self.walk_through_tile = walk_through_tile
        self.current_path = current_path

    @property
    def x(self):
        """
        Returns creature's x coord

        Returns:
            Creature's x coord
        """
        return self.owner.x

    @property
    def y(self):
        """
        Returns creature's y coord

        Returns:
            Creature's y coord
        """
        return self.owner.y

    def take_damage(self, damage):
        """
        Creature takes damage to hp and if hp is <= 0 and killable == True, it dies
        """
        self.hp -= damage
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + " took " + str(damage) + " damage", RED)
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + "'s hp is at :" + str(self.hp), WHITE)

        self.owner.game.particles.add(DamageNumParticle(self.x, self.y, damage, self.owner.game.particles))

        if self.hp <= 0 and self.killable:
            self.die()

    def die(self):
        """
        Prints that object is dead and removes it from all_creature and enemies group
        """
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + " is dead", BLUE)
        self.owner.game.all_creature.remove(self.owner)
        self.owner.game.GAME_OBJECTS.remove(self.owner)
        self.owner.game.enemy_group.remove(self.owner)

    def move(self, dx, dy):
        """
        Moves entity's position if tile is not a tile or enemy
        else do nothing if wall or attack if enemy

        Moves entity by dx and dy on map. If entity collides with
        wall or enemy, stop it from moving by actually reversing the move

        Args:
            dx (int): int to change entity's x coord
            dy (int): int to change entity's y coord
        """
        self._update_anim_status(dx, dy)

        self.owner.x += dx
        self.owner.y += dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

        if not self.walk_through_tile:
            # check to see if entity collided with wall and if so don't move
            creature_collide_with_wall = pygame.sprite.spritecollideany(
                self.owner, self.owner.game.walls)

            if creature_collide_with_wall:
                self.reverse_move(dx, dy)

        # check to see if entity collided with enemy and if so don't move
        if self.enemy_group:
            creature_hit = pygame.sprite.spritecollideany(self.owner, self.enemy_group)
            if creature_hit:
                self.reverse_move(dx, dy)
                self.attack(creature_hit, 1)

    def _update_anim_status(self, dx, dy):
        """
        Updates the direction the sprite is moving

        If sprite is moving regardless of direction, moving is true.
        If sprite is moving left, left = True and right = False and
        opposite is true for moving right

        Args:
            dx (int): change in x
            dy (int): change in y
        """
        if dx > 0:
            self.owner.right = True
            self.owner.left = False
            self.owner.moving = True
        elif dx < 0:
            self.owner.right = False
            self.owner.left = True
            self.owner.moving = True

        if not dy == 0:
            self.owner.moving = True

    def reverse_move(self, dx, dy):
        """
        Reverse the move

        Args:
            dx (int): int to change entity's x coord
            dy (int): int to change entity's y coord
        """
        self.owner.x -= dx
        self.owner.y -= dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

    def attack(self, target, damage):
        """
        Attack target creature for damage

        Args:
            target (object): object to attack
            damage (int): damage to do to object
        """
        self.owner.game.drawing.add_game_message_to_print(self.name_instance + " attacks " + target.creature.name_instance
                                                          + " for " + str(damage) + " damage", WHITE)
        target.creature.take_damage(damage)