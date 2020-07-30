import random

from constant import SLIME_FOV


def _calculate_change_in_position(diff):
    """
    Helper function for take_turn. Returns int that moves
    self closer to player

    Args:
        diff (int): difference between self position and player
    """
    if (diff > 0):
        move = -1
    elif (diff < 0):
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


class SmartAi:
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
        x_coord = creature.x
        y_coord = creature.y
        player_x = self.owner.game.player.x
        player_y = self.owner.game.player.y
        # Diff in monster and player coord
        diff_x = x_coord - player_x
        diff_y = y_coord - player_y

        # If player is not in enemy FOV wander
        if (abs(diff_x) > SLIME_FOV or abs(diff_y) > SLIME_FOV):
            creature.move(random.choice(
                [0, 1, -1]), random.choice([0, 1, -1]))
        # Else move towards player using shortest path
        else:
            # Find path to player if no path creature has no path calculated
            if (not creature.current_path):
                start = (x_coord, y_coord)
                goal = (player_x, player_y)
                visited = self.owner.game.graph.bfs(start, goal)

                if (visited):
                    path = self.owner.game.graph.find_path(start, goal, visited)
                    creature.current_path = path

            dest = creature.current_path.pop(0)
            dest_x = dest[0] - x_coord
            dest_y = dest[1] - y_coord

            creature.move(dest_x, dest_y)