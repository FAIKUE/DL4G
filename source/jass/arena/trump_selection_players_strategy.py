# HSLU
#
# Created by Thomas Koller on 05.09.18
#

from source.jass.base.const import PUSH, DIAMONDS, MAX_TRUMP
from source.jass.arena.trump_selection_strategy import TrumpStrategy
import logging


class TrumpPlayerStrategy(TrumpStrategy):

    def __init__(self):
        self._logger = logging.getLogger(__name__)

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
        if trump_action < DIAMONDS or (trump_action > MAX_TRUMP and trump_action != PUSH):
            self._logger.error('Illegal trump (' + str(trump_action) + ') selected')
            raise RuntimeError('Illegal trump (' + str(trump_action) + ') selected')
        rnd.action_trump(trump_action)
        if trump_action == PUSH:
            # ask second player
            player_rnd.set_from_round(rnd)
            trump_action = arena.players[player_rnd.player].select_trump(player_rnd)
            if trump_action < DIAMONDS or trump_action > MAX_TRUMP:
                self._logger.error('Illegal trump (' + str(trump_action) + ') selected')
                raise RuntimeError('Illegal trump (' + str(trump_action) + ') selected')
            rnd.action_trump(trump_action)
