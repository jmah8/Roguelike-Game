import json
import os

import draw
from constant import *
import config
import game as g
import pygame
import particle


def diagonal_distance(start, end):
    """
    Finds the diagonl distance between start and end

    Taken from:
        https://www.redblobgames.com/grids/line-drawing.html

    Args:
        start ((int, int)): Start of line to calculate diagonal distance
        end ((int, int)): End of line to calculate diagonal distance

    Returns:
        distance (int): Diagonal distance between start and end
    """
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    return distance


def round_point(position):
    """
    Rounds float to int

    Taken from:
        https://www.redblobgames.com/grids/line-drawing.html

    Args:
        position ((int, int)): Position to round to int

    Returns:
        p ((int, int)): Rounded position
    """
    p = round(position[0]), round(position[1])
    return p


def lerp_point(start, end, t):
    """
    Returns position between start and end,
    depending on t

    Taken from:
        https://www.redblobgames.com/grids/line-drawing.html

    Args:
        start ((int, int)): Start point of line
        end ((int, int)): End point of line
        t (int): Number that decides what position to choose

    Returns:
        position ((int, int)): Position between start and end,
        depending on t
    """
    x1, y1 = start
    x2, y2 = end
    c1 = lerp(x1, x2, t)
    c2 = lerp(y1, y2, t)
    position = c1, c2
    return position


def lerp(num1, num2, t):
    """
    Gives number between num1 and num2,
    depending on t

    Taken from:
        https://www.redblobgames.com/grids/line-drawing.html
    
    Args:
        num1 (int): First number to choose number between
        num2 (int): Second number to choose number between
        t (int): Number that decides what number to choose

    Returns:
        num (int): Number between num1 and num2, depending on t
    """
    num = num1 + t * (num2 - num1)
    return num


def line(start, end, map):
    """
    Draws line from start to end, stopping at any wall,
    returning the tiles the line passes through

    Taken from:
        https://www.redblobgames.com/grids/line-drawing.html

    Args:
        start ((int, int)): Start position of line
        end ((int, int)): End position of line
        map (2D array): Array of map

    Returns:
        points (List): List of points line passed through
    """
    points = []
    num_of_tiles = diagonal_distance(start, end)
    for i in range(num_of_tiles + 1):
        if num_of_tiles == 0:
            t = 0
        else:
            t = i / num_of_tiles
        x, y = round_point(lerp_point(start, end, t))
        if map[y][x].type == WALL:
            break
        # Skip the point the entity is on
        if i != 0:
            points.append((x, y))
    return points


def cast_fireball(game, caster, line):
    """
    Throws fireball following line stopping at first enemy hit.
    
    Args:
        game (Game): Game with game data
        caster (Object): Creature that casted fireball
        line (List): List of coordinates for fireball to follow
    """
    base_damage = data["fireball"]["damage"]
    mp_cost = data["fireball"]["cost"]

    particle_group = []
    particle.MagicParticle(particle_group, config.SPRITE.magic['fireball'], line)

    damage = caster.creature.stat.calc_magic_damage(base_damage)

    # If caster has enough mp to cast magic
    if caster.creature.stat.mp - mp_cost >= 0:
        caster.creature.stat.mp -= mp_cost
        # get list of tiles from start to end
        enemies = []
        for team, entity in config.GAME_DATA.creature_data.items():
            if team != caster.creature.team:
                enemies += entity
        creature_hit = False
        for (x, y) in line:
            if creature_hit:
                break
            # damage first enemy in list of tile
            for enemy in enemies:
                if (enemy.x, enemy.y) == (x, y):
                    caster.creature.attack(enemy, damage)
                    creature_hit = True
                    break

            _update_spell(game, particle_group)


def _update_spell(game, particle_group):
    """
    Updates the spell casted

    Args:
        game (Game): Game with all game data
        particle_group (List): List of particles
    """
    game.update()
    for magic in particle_group:
        draw.draw_at_camera_offset_with_image(magic)
        magic.update()
    config.CLOCK.tick(20)
    pygame.display.update()


# TODO: make it so enemies wont target through their allies
def cast_lightning(game, caster, line):
    """
    Throws lightning following line, hitting all enemies in path.

    Args:
        game (Game): Game with game data
        caster (Object): Creature that casted lightning
        line (List): List of coordinates for lightning to follow
    """
    base_damage = data["lightning"]["damage"]
    mp_cost = data["lightning"]["cost"]

    particle_group = []
    particle.MagicParticle(particle_group, config.SPRITE.magic['lightning'], line)

    damage = caster.creature.stat.calc_magic_damage(base_damage)

    # If caster has enough mp to cast magic
    if caster.creature.stat.mp - mp_cost >= 0:
        caster.creature.stat.mp -= mp_cost
        # get list of tiles from start to end
        enemies = []
        for team, entity in config.GAME_DATA.creature_data.items():
            if team != caster.creature.team:
                enemies += entity
        for (x, y) in line:
            for enemy in enemies:
                if (enemy.x, enemy.y) == (x, y):
                    caster.creature.attack(enemy, damage)

            _update_spell(game, particle_group)


with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/magic.json')) as f:
    data = json.load(f)
