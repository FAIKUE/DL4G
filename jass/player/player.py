from jass.base.player_round import PlayerRound


class Player:
    """ Player is the abstract base class for all Jass player implementations. """

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump, int encoded as defined in jass.base.const.trump_ints or jass.base..const.PUSH
        """
        raise Exception("not implemented")

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, str encoded as defined in jass.base.const.card_strings
        """
        raise Exception("not implemented")
