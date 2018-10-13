# HSLU
#
# Created by Thomas Koller on 06.09.18
#

from jass.base.player_round import PlayerRound
from jass.base.round import Round


def validate_round(rnd: Round):
    """
    Validate all tricks (and all moves in the tricks) for a round to verify that the played card is included
    in the valid card set. The round must contain the information about all the played cards.
    Args:
        rnd: a complete round
    """
    player_rnds = PlayerRound.all_from_complete_round(rnd)
    for i, player_rnd in enumerate(player_rnds):
        nr_trick, move_in_trick = divmod(i, 4)
        card_played = rnd.tricks[nr_trick, move_in_trick]
        validate_player_round(player_rnd, card_played)


def validate_player_round(player_rnd: PlayerRound, card_played: int) -> None:
    """
    Validate that the played card is among the valid cards for that round. An assertion error is thrown
    if that is not the case
    Args:
        player_rnd: the player round that is validated
        card_played: the actual card played
    """
    valid_cards = player_rnd.get_valid_cards()
    assert valid_cards[card_played] == 1
