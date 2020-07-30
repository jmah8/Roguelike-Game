import random

from constant import SLIME_FOV


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
            move_x = self._calculate_change_in_position(diff_x)
            move_y = self._calculate_change_in_position(diff_y)

            self.owner.creature.move(move_x, move_y)

    def _calculate_change_in_position(self, diff):
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