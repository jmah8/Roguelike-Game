from constant import *
import config
import random



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

    # TODO: make it so that enemies dont get block by other enemies
    #       even though there is space to move around
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
            self._make_path_to_player(creature, player)

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
        visited = config.PATHFINDING.bfs(start, goal)
        if visited:
            path = config.PATHFINDING.find_path(start, goal, visited)
            creature.current_path = path
