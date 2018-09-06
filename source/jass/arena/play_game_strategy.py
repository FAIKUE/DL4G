# HSLU
#
# Created by Thomas Koller on 05.09.18
#


class PlayGameStrategy:
    """
    Strategy to play a number of rounds until the game is complete.
    """
    def play_game(self, arena) -> None:
        """
        Play a game and determine the winners and points. Must be overridden in derived class.
        Args:
            arena: the arena for which to play the game.

        """
        raise NotImplementedError
