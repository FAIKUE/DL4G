# HSLU
#
# Created by Thomas Koller on 31.12.17

""" Implementation of rules of jass game"""

import numpy as np
from jass.base.round import Round
from jass.base.player_round import PlayerRound


class Rule:
    """
    Class for implementing rules of the jass game. The class includes rules that depend not on the process (like
    how trump is determined), but only upon cards. Currently this includes to determine the valid cards to play
    in a trick, to determine the winner of a trick and the points of a trick.

    This in an abstract base class that defines the interface.
    """

    def get_valid_cards(self, hand: np.array, current_trick: np.ndarray or list, move_nr: int, trump: int or None) -> np.array:
        """
        Get the valid cards that can be played by the current player.

        Args:
            hand: one-hot encoded array of hands owned by the player
            current_trick: array with the indices of the cards for the previous moves in the current trick
            move_nr: which move the player has to make in the current trick, 0 for first move, 1 for second and so on
            trump: trump color (if used by the rule)

        Returns:
            one-hot encoded array of valid moves
        """
        raise NotImplementedError()

    def calc_points(self, trick: np.ndarray, is_last: bool, trump: int = -1) -> int:
        """
        Calculate the points from the cards in the trick. Must be implemented in subclass

        Args:
            trick: the trick
            is_last: true if this is the last trick
            trump: the trump for the round (if needed by the rules)
        """
        raise NotImplementedError

    def calc_winner(self, trick: np.ndarray, first_player: int, trump: int = -1) -> int:
        """
        Calculate the winner of a completed trick. Must be implemented in subclass.

        Precondition:
            0 <= trick[i] <= 35, for i = 0..3
        Args:
            trick: the completed trick
            first_player: the first player of the trick
            trump: the trump for the round (if needed by the rules)

        Returns:
            the player who won this trick
        """
        raise NotImplementedError

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
