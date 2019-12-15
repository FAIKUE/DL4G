# HSLU
#
# Created by Thomas Koller on 19.07.19
#
import numpy as np

from source.jass.base.const import next_player
from source.jass.base.player_round import PlayerRound
from source.jass.base.round import Round


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


def calculate_hands_from_starting_hands(player_rnd: PlayerRound, starting_hands: np.ndarray) -> np.ndarray:
    """
    Calculate the hands of each player from the starting hands for a specific player round.
    Args:
        player_rnd: the player round
        starting_hands: hands of the players at the beginning of the game

    Returns:
        the hands of the player at the point in the game specified by the player_rnd
    """
    hands = starting_hands.copy()
    for card_nr in range(player_rnd.nr_played_cards):
        # card played
        card_played = player_rnd.tricks[divmod(card_nr, 4)]
        # clear card (for all players)
        hands[:, card_played] = 0

    assert hands.sum() == 36 - player_rnd.nr_played_cards

    return hands
