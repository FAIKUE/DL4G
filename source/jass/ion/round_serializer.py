# HSLU
#
# Created by Thomas Koller on 24.08.18
#

import logging
from source.jass.base.const import convert_int_encoded_cards_to_str_encoded, partner_player, next_player, card_ids
from source.jass.base.round import Round
from source.jass.base.round_factory import get_round

# format of date for reading and writing
DATE_FORMAT = '%d.%m.%y %H:%M:%S'


class RoundSerializer:
    """
    Class for generation and parsing of the dict/json representation of a Round.
    """
    @staticmethod
    def round_to_dict(rnd: Round) -> dict:
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
        data['player'] = rnd.player

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

        data['jassTyp'] = rnd.jass_type
        return data

    @staticmethod
    def round_from_dict(round_dict: dict) -> Round or None:
        """
        Generate a round from a dict representation
        Args:
            round_dict: dict representation of round

        Returns:
            a round
        """

        # check a mandatory field to see if it seems a valid entry
        if 'trump' not in round_dict:
            logging.getLogger(__name__).warning('Warning: no trump found in entry: {}'.format(round_dict))
            return None

        rnd = get_round(round_dict['jassTyp'], round_dict['dealer'])
        rnd.trump = round_dict['trump']

        if 'tss' in round_dict and round_dict['tss'] == 1:
            rnd.forehand = False
            rnd.declared_trump = partner_player[next_player[rnd.dealer]]
        else:
            rnd.forehand = True
            rnd.declared_trump = next_player[rnd.dealer]

        tricks = round_dict['tricks']

        # games might be incomplete (less than 9 tricks), we only use complete games
        if len(tricks) != 9:
            # print('Skipping incomplete game: {} tricks'.format(len(g.tricks)))
            return None

        for i, trick_dict in enumerate(tricks):
            rnd.trick_winner[i] = trick_dict['win']
            rnd.trick_first_player[i] = trick_dict['first']
            cards = trick_dict['cards']
            rnd.tricks[i, 0] = card_ids[cards[0]]
            rnd.tricks[i, 1] = card_ids[cards[1]]
            rnd.tricks[i, 2] = card_ids[cards[2]]
            rnd.tricks[i, 3] = card_ids[cards[3]]
            rnd.trick_points[i] = trick_dict['points']
            if rnd.trick_winner[i] == 0 or rnd.trick_winner[i] == 2:
                rnd.points_team_0 += rnd.trick_points[i]
            else:
                rnd.points_team_1 += rnd.trick_points[i]

        if 'player' in round_dict:
            rnd.player = round_dict['player']
        else:
            rnd.player = None

        # complete entry
        rnd.nr_tricks = 9
        rnd.nr_played_cards = 36
        rnd.current_trick = None

        return rnd
