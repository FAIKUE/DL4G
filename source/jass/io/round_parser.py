# HSLU
#
# Created by Thomas Koller on 24.08.18
#
import json

from jass.base.const import *
from jass.base.round import Round
from jass.base.round_factory import get_round


class RoundParser:
    """
    Class to parse a Round from dict/json. While the format used for the round information is the same as for the
    log files, additional data can be parsed for the players and the date (both optionally). These will be added
    as json.
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

        rnd = get_round(data['jass_typ'], data['dealer'])
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

        # end of game, there should be no player, but we take what is on the file as to be compatible to the log file
        # format
        if 'player' in data:
            rnd.player = data['player']
        else:
            rnd.player = None

        # current trick should be the trick at the end of the game
        #rnd.current_trick = rnd.tricks[8, :]
        # no current trick at the end of a game
        rnd.current_trick = None

        return rnd

    @staticmethod
    def parse_round_all(data: dict):
        """
        Parse dict to reconstruct a round and additional data like date and players.
        Returns:
            a tuple of round, date and players
        """
        rnd = RoundParser.parse_round(data)
        if 'date' in data:
            date = data['date']
        else:
            date = None

        if 'players' in data:
            players = data['players']
        else:
            players = None

        return rnd, date, players

    @staticmethod
    def parse_rounds_from_file(filename: str):
        """
        Parse all rounds in a file and return them
        Args:
            filename: the filename to parse

        Returns:
            a list of rounds
        """
        rnds = []
        with open(filename, "r") as file:
            # each line contains one round
            for line in file:
                # get the line first as dict
                round_dict = json.loads(line)
                rnd = RoundParser.parse_round(round_dict)
                rnds.append(rnd)

        return rnds

