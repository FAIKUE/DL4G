# HSLU
#
# Created by Thomas Koller on 14.08.18
#
"""
Statistics about valid cards that can be played, that will show the number of valid cards as a function of the cards
 already played.
"""

import numpy as np
from source.jass.base.player_round import PlayerRound
from source.jass.base.round import Round


class ValidCardsStat:
    """
    Calculate statistics about the number of valid cards from player rounds that are obtained from a full round.
    """
    def __init__(self):
        # the total of valid card moves per move number (cards played)
        self.valid_moves_sum = np.zeros(36, np.int64)
        self.nr_total_moves = np.zeros(36, np.int64)

    def add_round(self, rnd: Round) -> None:
        """
        Add the statistics from a complete round (36 cards played)
        Args:
            rnd: complete round
        """
        player_rnds = PlayerRound.all_from_complete_round(rnd)
        for i, player_rnd in enumerate(player_rnds):
            valid_cards = player_rnd.get_valid_cards()
            self.valid_moves_sum[i] += np.sum(valid_cards)
            self.nr_total_moves[i] += 1

    def add_player_round(self, player_rnd: PlayerRound) -> None:
        valid_cards = player_rnd.get_valid_cards()
        self.valid_moves_sum[player_rnd.nr_played_cards] += np.sum(valid_cards)
        self.nr_total_moves[player_rnd.nr_played_cards] += 1

    def get_stats(self):
        """
        Get the computed statistics.

        Returns:
            The average number of valid card actions.
        """
        return self.valid_moves_sum / self.nr_total_moves

    def get(self) -> dict:
        return dict(valid=self.get_stats().tolist())
