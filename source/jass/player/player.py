from source.jass.base.player_round import PlayerRound


class Player:
    """ Player is the abstract base class for all Jass player implementations. """

    def select_trump(self, rnd: PlayerRound) -> int or None:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump, int encoded as defined in source.jass.base.const or source.jass.base.const.PUSH
        """
        raise NotImplementedError()

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded as defined in source.jass.base.const
        """
        raise NotImplementedError()
