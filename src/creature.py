from particle import *
import json


class CreatureStat:

    def __init__(self, hp, mp, strength, dexterity, intelligence, level=1):
        """
        Stats of a creature

        Args:
            hp (int): hp of creature
            mp (int): mp of creature
            strength (int): strength of creature
            dexterity (int): dexterity of creature
            intelligence (int): intelligence of creature
            level (int): level of creature

        Attributes:
            exp (int): experience points creature has
        """
        self.max_hp = hp
        self.max_mp = mp
        self.hp = hp
        self.mp = mp
        self.level = level
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

    def calc_damage(self):
        """
        Return damage dealt scaling with level and strength

        Returns:
            damage (int): damage entity with stat will do

        """
        damage = (self.level + self.strength) // 2
        return damage


class Creature:
    """
    have hp
    can damage other objects
    can die

    Attributes:
        name_instance (arg, string) : Name of creature
        stat (arg, int) : stat of creature
        owner (object) : object that has self as creature component
        killable (arg, boolean) : if creature is killable
        enemy_group (arg, group): group creature can attack
        walk_through_tile (arg, boolean): if creature can walk through tiles like walls
        current_path (arg, List): List of path from start to goal
    """

    def __init__(self, name_instance, killable=None, enemy_group=None, walk_through_tile=False, current_path=None):
        self.name_instance = name_instance
        self.owner = None
        self.killable = killable
        self.enemy_group = enemy_group
        self.walk_through_tile = walk_through_tile
        self.current_path = current_path
        self.stat = self._load_stat()

    def _load_stat(self):
        """
        Loads stat specific to creature of name_instance and returns it

        Returns:
            stat (Stat): Stat of creature with name_instance
        """
        with open('./data/creature.json') as f:
            data = json.load(f)

        if self.name_instance in data.keys():
            str = data[self.name_instance]
            stat = CreatureStat(str["hp"], str["mp"], str["strength"],
                        str["dexterity"], str["intelligence"])
            return stat

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
        self.stat.hp -= damage
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + " took " + str(damage) + " damage", RED)
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + "'s hp is at :" + str(self.stat.hp), WHITE)

        DamageNumParticle(self.x, self.y, damage, self.owner.game.particles)

        if self.stat.hp <= 0 and self.killable:
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

        Checks if thing self is moving into is a wall or enemy and
        if it is don't move and do nothing or attack respectively

        Args:
            dx (int): int to change entity's x coord
            dy (int): int to change entity's y coord
        """
        self._update_anim_status(dx, dy)

        if not self.walk_through_tile:
            # check to see if entity collided with wall and if so don't move
            for wall in self.owner.game.walls:
                if (wall.x, wall.y) == (self.x + dx, self.y + dy):
                    return

        # check to see if entity collided with enemy and if so don't move
        if self.enemy_group:
            for enemy in self.enemy_group:
                if (enemy.x, enemy.y) == (self.x + dx, self.y + dy):
                    self.attack(enemy, self.stat.calc_damage())
                    return

        self.owner.x += dx
        self.owner.y += dy
        self.owner.rect.topleft = (
            self.owner.x * SPRITE_SIZE, self.owner.y * SPRITE_SIZE)

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

    def attack(self, target, damage):
        """
        Attack target creature for damage

        Args:
            target (object): object to attack
            damage (int): damage to do to object
        """
        self.owner.game.drawing.add_game_message_to_print(
            self.name_instance + " attacks " + target.creature.name_instance
            + " for " + str(damage) + " damage", WHITE)
        target.creature.take_damage(damage)
