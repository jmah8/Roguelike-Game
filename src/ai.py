import random

from constant import *


def _calculate_change_in_position(diff):
    """
    Helper function for take_turn. Returns int that moves
    self closer to player

    Args:
        diff (int): difference between self position and player
    """
    if diff > 0:
        move = -1
    elif diff < 0:
        move = 1
    else:
        move = 0
    return move


class Ai_test:
    """
    Once per turn, execute
    """

    def __init__(self):
        self.owner = None

    def take_turn(self):
        """
        Make creature move towards the player if in creature FOV,
        else wander
        """
        diff_x = self.owner.x - self.owner.game.player.x
        diff_y = self.owner.y - self.owner.game.player.y

        # If player is not in enemy FOV wander
        if (abs(diff_x) > SLIME_FOV or abs(diff_y) > SLIME_FOV):
            self.owner.creature.move(random.choice(
                [0, 1, -1]), random.choice([0, 1, -1]))
        # Else move towards player using shortest path
        else:
            move_x = _calculate_change_in_position(diff_x)
            move_y = _calculate_change_in_position(diff_y)

            self.owner.creature.move(move_x, move_y)


class ChaseAI:
    """
    Once per turn, execute

    Attributes:
        owner (Object): owner of ai
    """

    def __init__(self):
        self.owner = None

    def take_turn(self):
        """
        Make creature move towards the player if in creature FOV,
        else wander
        """
        creature = self.owner.creature
        player = self.owner.game.player
        diff_x = creature.x - player.x
        diff_y = creature.y - player.y

        # If player is not in enemy FOV wander
        if abs(diff_x) > SLIME_FOV or abs(diff_y) > SLIME_FOV:
            creature.move(random.choice(
                [0, 1, -1]), random.choice([0, 1, -1]))
        # Else move towards player using shortest path
        else:
            # Find path to player if no path creature has no path calculated
            if not creature.current_path:
                self._make_path_to_player(creature, player)

            # TODO: make it so when dest x/y is > 1, recalculate path
            dest = creature.current_path.pop(0)
            dest_x = dest[0] - creature.x
            dest_y = dest[1] - creature.y

            creature.move(dest_x, dest_y)

    def _make_path_to_player(self, creature, player):
        """
        Makes path to player

        Args:
            creature (Creature): Creature to make path for
            player (Creature): The player the creature paths to
        """
        start = (creature.x, creature.y)
        goal = (player.x, player.y)
        visited = self.owner.game.graph.bfs(start, goal)
        if visited:
            path = self.owner.game.graph.find_path(start, goal, visited)
            creature.current_path = path
