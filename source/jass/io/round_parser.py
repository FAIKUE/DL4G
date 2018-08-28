# HSLU
#
# Created by Thomas Koller on 24.08.18
#

from jass.base.const import *
from jass.base.round import Round


class RoundParser:
    """
    Class to parse a Round from dict/json
    """
    @staticmethod
    def parse_round(data: dict) -> Round or None:
        """
        Parse a dict to reconstruct a Round
        Args:
            data: dict containing the round data

        Returns:
            the round or None if the round does not contain a full game
        """
        # check a mandatory field to see if it seems a valid entry

        rnd = Round()
        rnd.dealer = data['dealer']
        rnd.trump = data['trump']

        if 'tss' in data and data['tss'] == 1:
            rnd.forehand = False
            rnd.declared_trump = partner_player[next_player[rnd.dealer]]
        else:
            rnd.forehand = True
            rnd.declared_trump = next_player[rnd.dealer]

        tricks = data['tricks']

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

        # complete entry
        rnd.nr_tricks = 9
        rnd.nr_played_cards = 36

        # current trick should be the trick at the end of the game
        rnd.current_trick = rnd.tricks[8,:]

        return rnd
