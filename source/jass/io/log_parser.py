# Copyright 2017 HSLU. All Rights Reserved.
#
# Created by Thomas Koller on 01.12.17
#
#

"""
Parse the log files containing the game play data
"""

import json
import logging
from typing import Optional, List, Dict
from jass.base.const import *
from jass.base.round import Round
from jass.base.round_factory import get_round


class LogParser:
    """
    Class to parse the log files.
    """
    def __init__(self, filename: str or None) -> None:
        """
        Initialise the parser with the given filename. The parsing is not done during initialisation, but
        only after parse_rounds is called.

        Args:
            filename:
        """
        self._filename = filename
        self._logger = logging.getLogger(__name__)

    def parse_rounds(self) -> List[Round]:
        rnds = []
        with open(self._filename, 'r') as file:
            nr_lines = 0
            nr_rounds = 0
            nr_skipped = 0
            # one line contains one log record (with multiple rounds)
            for line in file:
                nr_lines += 1
                # start of line contains:
                # 27.11.17 20:10:08,140 | INFO |  |  |  |  |
                # so we read until the first {
                index = line.find('{')
                if index:
                    line_json = json.loads(line[index:])
                    # read the players for those rounds
                    for r in line_json['rounds']:
                        if r is not None:
                            rnd_read = self.read_round(r)
                            if rnd_read is not None:
                                nr_rounds += 1
                                rnds.append(rnd_read)
                            else:
                                nr_skipped += 1

        self._logger.info('Read {} valid rounds from file'.format(nr_rounds))
        self._logger.info('Skipped {} rounds'.format(nr_skipped))
        return rnds

    def parse_rounds_and_players(self) -> List[Dict]:
        rnds = []
        with open(self._filename, 'r') as file:
            nr_lines = 0
            nr_rounds = 0
            nr_skipped = 0
            # one line contains one log record (with multiple rounds)
            for line in file:
                nr_lines += 1
                # start of line contains:
                # 27.11.17 20:10:08,140 | INFO |  |  |  |  |
                # so we read until the first {
                index = line.find('{')
                if index:
                    line_json = json.loads(line[index:])
                    # read the players for those rounds
                    if 'players' in line_json:
                        players = line_json['players']
                    else:
                        players = [0, 0, 0, 0]
                    for r in line_json['rounds']:
                        if r is not None:
                            rnd_read = self.read_round(r)
                            if rnd_read is not None:
                                nr_rounds += 1
                                rnds.append(dict(players=players, round=rnd_read))
                            else:
                                nr_skipped += 1

        self._logger.info('Read {} valid rounds from file'.format(nr_rounds))
        self._logger.info('Skipped {} rounds'.format(nr_skipped))
        return rnds


    def read_round(self, round_dict: dict) -> Optional[Round]:
        """
        Read a round (game) from the parsed log file and return it
        Args:
            round_dict: Dict containing the parsed round from the log file
        Returns:
            Round with the data from the round
        """

        # check a mandatory field to see if it seems a valid entry
        if 'trump' not in round_dict:
            self._logger.warning('Warning: no trump found in entry: {}'.format(round_dict))
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

        # complete entry
        rnd.nr_tricks = 9
        rnd.nr_played_cards = 36

        return rnd
