# HSLU
#
# Created by Thomas Koller on 05.09.18
#

from source.jass.arena.trump_selection_strategy import TrumpStrategy


class TrumpNoneStrategy(TrumpStrategy):
    """
    Strategy to not select a trump (for jass types that do not need a trump)
    """

    def determine_trump(self, rnd, arena):
        """
        Do not change the round.
        Args:
            rnd: the round for which to determine trump.
            arena: the arena to which this strategy belongs, needed to access the players and possibly other data
        """
    pass
