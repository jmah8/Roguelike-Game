import os
import json
import config
from particle import *
import game_text

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/creature.json')) as f:
    data = json.load(f)


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
            exp (int): experience points creature has (in percent)
        """
        self.max_hp = hp + (5 * (level - 1))
        self.max_mp = mp + (3 * (level - 1))
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.exp = 0
        self.level = level
        self.strength = strength + (1 * (level - 1))
        self.dexterity = dexterity + (1 * (level - 1))
        self.intelligence = intelligence + (1 * (level - 1))

    def level_up(self):
        self.max_hp += 5
        self.max_mp += 3
        self.strength += 1

    def calc_phys_damage(self):
        """
        Return damage dealt from hitting,
        scaling with level and strength

        Returns:
            damage (int): damage self with stat will do

        """
        damage = (self.level + self.strength) // 2
        return damage

    def calc_magic_damage(self, base_damage):
        """
        Returns damage dealt from using spell
        scaling with level and intelligence

        Args:
            base_damage (int): base damage of spell

        Returns:
            damage (int): damage spell will do when casted by self
        """
        damage = (self.level + self.intelligence) * base_damage // 2
        return damage

    def calc_exp_gained_from_self(self, player_level):
        """
        Returns exp gained from player slaying self.

        Level gained is based on difference in levels.
        With larger increase in exp when player is >=
        level of self

        Args:
            player_level (int): Level of thing that slayed self

        Returns:
            exp_gained (int): exp gained by slayer
        """
        if player_level > self.level:
            scale = 5
        else:
            scale = 20

        exp_gained = abs(player_level - self.level) + 1 * scale
        return exp_gained

class Creature:
    """
    have hp
    can damage other objects
    can die

    Args:
        level (int): level of monster

    Attributes:
        name_instance (arg, string) : Name of creature
        stat (arg, int) : stat of creature
        owner (object) : Entity that has self as creature component
        killable (arg, boolean) : if creature is killable
        team (arg, group): team of self
        walk_through_tile (arg, boolean): if creature can walk through tiles like walls
        current_path (arg, List): List of path from start to goal
    """

    def __init__(self, name_instance, killable=None, team="enemy", walk_through_tile=False, current_path=None, level=1):
        self.name_instance = name_instance
        self.owner = None
        self.killable = killable
        self.team = team
        self.walk_through_tile = walk_through_tile
        self.current_path = current_path
        self.stat = self._load_stat(level)

    def _load_stat(self, level):
        """
        Loads stat specific to creature of name_instance and returns it

        Args:
            level (int): level of self

        Returns:
            stat (Stat): Stat of creature with name_instance
        """

        if self.name_instance in data.keys():
            str = data[self.name_instance]
            stat = CreatureStat(str["hp"], str["mp"], str["strength"],
                                str["dexterity"], str["intelligence"],
                                level)
            return stat

        return None

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

        Returns:
            bool: if creature died return true else return false
        """
        self.stat.hp -= damage
        game_text.add_game_message_to_print(
            self.name_instance + " took " + str(damage) + " damage", RED)
        game_text.add_game_message_to_print(
            self.name_instance + "'s hp is at :" + str(self.stat.hp), WHITE)

        NumberParticle(self.x, self.y, damage, config.PARTICLE_LIST, RED)

        if self.stat.hp <= 0 and self.killable:
            self.die()
            return True

        return False

    def die(self):
        """
        Prints that Entity is dead and removes it from config.GAME_DATA.creature_data
        """
        game_text.add_game_message_to_print(
            self.name_instance + " is dead", BLUE)
        config.GAME_DATA.creature_data[self.team].remove(self.owner)

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
            if config.MAP_INFO.tile_array[self.y + dy][self.x + dx].type == WALL:
                return

        # check to see if entity collided with enemy or ally and if so don't move
        for team, entity_list in config.GAME_DATA.creature_data.items():
            for entity in entity_list:
                if (entity.x, entity.y) == (self.x + dx, self.y + dy):
                    if team == self.team:
                        return
                    else:
                        self.attack(entity, self.stat.calc_phys_damage())
                        return

        self.owner.x += dx
        self.owner.y += dy

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

        Gives exp if target dies

        Args:
            target (object): Entity to attack
            damage (int): damage to do to Entity
        """
        game_text.add_game_message_to_print(
            self.name_instance + " attacks " + target.creature.name_instance
            + " for " + str(damage) + " damage", WHITE)
        if target.creature.take_damage(damage):
            self.gain_exp(target)
            self.check_for_level_up()

    def gain_exp(self, enemy):
        """
        Enemy to gain exp from

        Args:
            enemy (Entity): Entity with creature stats to gain exp from
        """
        exp = enemy.creature.stat.calc_exp_gained_from_self(self.stat.level)
        self.stat.exp += exp
        NumberParticle(self.x, self.y, exp, config.PARTICLE_LIST, YELLOW)

    def regen(self):
        """
        Regenerates hp and mp of self depending on how many turns have passed
        """
        if config.TURN_COUNT % REGEN_TIME == 0:
            if self.stat.hp + 1 <= self.stat.max_hp:
                self.stat.hp += 1
            if self.stat.mp + 1 <= self.stat.max_mp:
                self.stat.mp += 1

    def check_for_level_up(self):
        """
        Levels self up
        """
        while self.stat.exp >= 100:
            self.stat.level += 1
            self.stat.exp -= 100
            game_text.add_game_message_to_print(
                self.name_instance + " leveled up ", YELLOW)


