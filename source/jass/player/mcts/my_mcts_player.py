from source.jass.base.const import *
from source.jass.base.player_round import PlayerRound
from source.jass.player.player import Player
from source.jass.base.rule_schieber import RuleSchieber
from source.jass.player.mcts.monte_carlo_tree_search import MonteCarloTreeSearch

import logging


class MyMCTSPlayer(Player):
    """
    Implementation of a player to play Jass using Monte Carlo Tree Search.
    """

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._rule = RuleSchieber()

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest points in cards
        best_trump = 0
        max_points_in_trump = 0
        for trump in trump_ints:
            points_in_trump = (rnd.hand * card_values[trump]).sum()
            if points_in_trump > max_points_in_trump:
                max_points_in_trump = points_in_trump
                best_trump = trump

        if max_points_in_trump < 49 and rnd.forehand is None:
            best_trump = PUSH
            print(f"Pushed trump selection to other player "
                  f"with {max_points_in_trump} points in the cards for the best trump")
        else:
            print(f"Selected trump {trump_strings_german_long[best_trump]} with {max_points_in_trump} points in the cards.")
        return best_trump

    def play_card(self, player_rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            player_rnd: current round

        Returns:
            card to play, int encoded
        """
        bestcard = MonteCarloTreeSearch.monte_carlo_tree_search_multisample_threading(player_rnd)

        return bestcard
