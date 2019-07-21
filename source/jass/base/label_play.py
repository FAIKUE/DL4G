# HSLU
#
# Created by Thomas Koller on 19.07.19
#
import numpy as np


class LabelPlay:
    """
    Class to define (possible) training information for a specific action in the game when it is in the playing
    stage (i.e. not in the trump defining stage).

    This includes the card played, the points made in the current trick by the own team and the other, the player who
    won the trick, the points made in the round by the own team and the other and the hands the players had at the
    beginning of the game.

    (Adding both the points for own and opposite team for the points in the trick eliminates needing to know the
    current player. Adding the information about the exact winner (instead of the team) might help to forecast the
    result of the trick)+

    """
    def __init__(self,
                 card_played: int,
                 points_in_trick_own: int,
                 points_in_trick_other: int,
                 trick_winner: int,
                 points_in_round_own: int,
                 points_in_round_other: int,
                 hands: np.ndarray):
        self.card_played = card_played
        self.points_in_trick_own = points_in_trick_own
        self.points_in_trick_other = points_in_trick_other
        self.trick_winner = trick_winner
        self.points_in_round_own = points_in_round_own
        self.points_in_round_other = points_in_round_other
        self.hands = hands
