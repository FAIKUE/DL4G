# HSLU
#
# Created by Thomas Koller on 05.09.18
#

import numpy as np

from jass.base.const import JASS_SCHIEBER_1000, JASS_SCHIEBER_2500, JASS_HEARTS
from jass.base.round import Round
from jass.base.round_schieber import RoundSchieber
from jass.base.round_hearts import RoundHeartsTeam
from jass.base.player_round import PlayerRound


def get_round(jass_type: str, dealer: int or None = None) -> Round:
    """
    Get the correct round object depending on the jass type
    Args:
        jass_type: the jass type
        dealer: dealer of the round

    Returns:
        the appropriate Round object for the type
    """
    if jass_type == JASS_SCHIEBER_1000:
        return RoundSchieber(dealer=dealer)
    elif jass_type == JASS_SCHIEBER_2500:
        return RoundSchieber(dealer=dealer, jass_type=jass_type)
    elif jass_type == JASS_HEARTS:
        return RoundHeartsTeam(dealer=dealer)
    else:
        raise ValueError('Type of jass unknown: {}'.format(jass_type))


def get_round_from_player_round(player_rnd: PlayerRound, hands: np.ndarray):
    """
    Create a round from a player round and the cards for the other player. All information from the player round
    is copied. The hands array must contain the correct number of cards for the state of the round. The hand of
    the current player is copied from the player_rnd and does not need to be in the hands array.
    Args:
        player_rnd: the player round
        hands: the other hands as a 4x36 hot-one encoded array

    Returns:
        a round with the correct information
    """
    # construct a round object
    rnd = get_round(player_rnd.jass_type, player_rnd.dealer)
    rnd.trump = player_rnd.trump
    rnd.declared_trump = player_rnd.declared_trump
    rnd.forehand = player_rnd.forehand
    rnd.player = player_rnd.player
    rnd.hands[:, :] = hands[:, :]
    rnd.tricks[:, :] = player_rnd.tricks[:, :]
    rnd.trick_winner[:] = player_rnd.trick_winner[:]
    rnd.trick_points[:] = player_rnd.trick_points[:]
    rnd.trick_first_player[:] = player_rnd.trick_first_player[:]
    rnd.nr_tricks = player_rnd.nr_tricks
    rnd.nr_cards_in_trick = player_rnd.nr_cards_in_trick
    rnd.nr_played_cards = player_rnd.nr_played_cards
    # current trick is a view into tricks
    rnd.current_trick = rnd.tricks[rnd.nr_tricks]

    rnd.points_team_0 = player_rnd.points_team_0
    rnd.points_team_1 = player_rnd.points_team_1
    rnd.jass_type = player_rnd.jass_type
    rnd.rule = player_rnd.rule

    return rnd
