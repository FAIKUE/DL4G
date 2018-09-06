# HSLU
#
# Created by Thomas Koller on 06.09.18
#

def get_valid_cards_from_player_round(self, player_rnd: PlayerRound):
    return self.get_valid_cards(player_rnd.hand,
                                player_rnd.current_trick,
                                player_rnd.nr_cards_in_trick,
                                player_rnd.trump)


def validate_round(self, rnd: Round):
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
        self.validate_player_round(player_rnd, card_played)


def validate_player_round(self, player_rnd: PlayerRound, card_played: int) -> None:
    """
    Validate that the played card is among the valid cards for that round. An assertion error is thrown
    if that is not the case
    Args:
        player_rnd: the player round that is validated
        card_played: the actual card played
    """
    valid_cards = self.get_valid_cards_from_player_round(player_rnd)
    assert valid_cards[card_played] == 1