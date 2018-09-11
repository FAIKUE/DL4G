# HSLU
#
# Created by Thomas Koller on 14.08.18
#
"""
Statistics about valid cards that can be played, that will show the number of valid cards as a function of the cards
 already played.
"""

import numpy as np
from jass.base.player_round import PlayerRound
from jass.base.round import Round


class ValidCardsStat:
    """
    Calculate statistics about the number of valid cards from player rounds that are obtained from a full round.
    """
    def __init__(self, rule):
        # the total of valid card moves per move number (cards played)
        self.valid_moves_sum = np.zeros(36, np.int64)
        self.nr_total_moves = 0
        self._rule = rule

    def add_round(self, rnd: Round) -> None:
        """
        Add the statistics from a complete round (36 cards played)
        Args:
            rnd: complete round
        """
        player_rnds = PlayerRound.all_from_complete_round(rnd)
        for i, player_rnd in enumerate(player_rnds):
            valid_cards = self._rule.get_valid_cards_from_player_round(player_rnd)
            self.valid_moves_sum[i] += np.sum(valid_cards)
        self.nr_total_moves += 1

    def get_stats(self):
        """
        Get the computed statistics.

        Returns:
            The average number of valid card actions.
        """
        return self.valid_moves_sum / self.nr_total_moves
