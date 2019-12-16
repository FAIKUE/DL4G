# HSLU
#
# Created by Thomas Koller on 05.09.18
#
import random
from jass.base.const import PUSH, MAX_TRUMP
from jass.arena.trump_selection_strategy import TrumpStrategy


class TrumpRandomStrategy(TrumpStrategy):
    """
    Strategy to select trump randomly.
    """

    def determine_trump(self, rnd, arena):
        """
        Determine trump (and push for first player) randomly
        Args:
            rnd: the round for which to determine trump.
            arena: the arena to which this strategy belongs, needed to access the players and possibly other data
        """
        # select randomly to push or not
        if random.randrange(2) == 1:
            rnd.action_trump(PUSH)

        # select random trump
        trump = random.randint(0, MAX_TRUMP)
        rnd.action_trump(trump)
