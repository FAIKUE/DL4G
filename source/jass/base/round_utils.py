# HSLU
#
# Created by Thomas Koller on 19.07.19
#
import numpy as np

from jass.base.const import next_player
from jass.base.round import Round


def calculate_starting_hands_from_round(rnd: Round) -> np.ndarray:
    """
    Calculate the hands of the players at the beginning of the game from a complete round
    Args:
        rnd: a complete rounds

    Returns:

    """
    hands = np.zeros(shape=[4, 36], dtype=np.int32)
    for rnd_nr in range(0, 9):
        player = rnd.trick_first_player[rnd_nr]
        for card_nr in range(4):
            card_played = rnd.tricks[rnd_nr, card_nr]
            hands[player, card_played] = 1
            player = next_player[player]
    return hands
