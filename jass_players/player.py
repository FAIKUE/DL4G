from jass_base.game import Round


class Player:
    """ Player is the abstract base class for all Jass player implementations. """

    def play_card(self, rnd: Round) -> str:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, encoded as defined in jass_base.game_const.card_strings
        """
        raise Exception("not implemented")

    def select_trump(self, rnd: Round) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump, encoded as defined in jass_base.game_const.trump_ints or jass_base.game_const.PUSH
        """
        raise Exception("not implemented")
