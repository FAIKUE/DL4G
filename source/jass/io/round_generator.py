# HSLU
#
# Created by Thomas Koller on 24.08.18
#

from jass.base.const import *
from jass.base.round import Round


class RoundGenerator:
    """
    Class for generation of the dict/json representation of Round
    """
    @staticmethod
    def generate_dict(rnd: Round) -> dict:
        """
        Generate dict for the player round that corresponds to the json description.

        We use the same format as defined by Swisslos for the log file for the json representation.

        Precondition:
            rnd must represent a full round of 36 cards played.

        Args:
            rnd: the round to convert

        Returns:
            dict representation of the round that can be converted to json
        """
        data = dict()

        if rnd.trump is not None:
            data['trump'] = int(rnd.trump)

        data['dealer'] = int(rnd.dealer)

        # tss only needs to be present if its value is 1
        if rnd.forehand is False:
            data['tss'] = 1

        # played tricks
        tricks = []

        # full tricks
        for i in range(rnd.nr_tricks):
            # cards of tricks
            cards_int = rnd.tricks[i, :].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(cards_int)
            trick = dict(
                cards=cards,
                points=int(rnd.trick_points[i]),
                win=int(rnd.trick_winner[i]),
                first=int(rnd.trick_first_player[i]))
            tricks.append(trick)

        data['tricks'] = tricks

        # there are no hands of players for full rounds, so we leave the 'player' information altogether and handle
        # it correspondingly in the parser
        # (it is not clear from the documentation if 'player' is mandatory)

        # also the Jass type is not really defined on the level of the round, so we leave it
        return data