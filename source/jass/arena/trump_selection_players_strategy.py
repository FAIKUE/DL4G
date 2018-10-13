# HSLU
#
# Created by Thomas Koller on 05.09.18
#

from jass.base.const import PUSH
from jass.arena.trump_selection_strategy import TrumpStrategy


class TrumpPlayerStrategy(TrumpStrategy):
    """
    Strategy to select trump by asking the players.
    """
    def determine_trump(self, rnd, arena):
        """
        Determine trump by asking the first player, and if he pushes the second player
        Args:
            rnd: the round for which to determine trump.
            arena: the arena to which this strategy belongs, needed to access the players and possibly other data
        """
        player_rnd = arena.get_player_round()

        # ask first player
        trump_action = arena.players[player_rnd.player].select_trump(player_rnd)
        rnd.action_trump(trump_action)

        if trump_action == PUSH:
            # ask second player
            player_rnd.set_from_round(rnd)
            trump_action = arena.players[player_rnd.player].select_trump(player_rnd)
            rnd.action_trump(trump_action)
