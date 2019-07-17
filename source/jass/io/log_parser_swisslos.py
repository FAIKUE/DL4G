# Copyright 2017 HSLU. All Rights Reserved.
#
# Created by Thomas Koller on 01.12.17
#
#

"""
Parse the log files containing the game play data in the data obtained from swisslos.
"""

import json
import logging
from typing import List
from datetime import datetime
from jass.io.round_log_entry import RoundLogEntry
from jass.io.round_serializer import DATE_FORMAT, RoundSerializer


class LogParserSwisslos:
    """
    Class to parse the log files.
    """

    @staticmethod
    def parse_rounds(filename) -> List[RoundLogEntry]:
        """
        Parse rounds including information about the players and the date which is stored in a list of objects.

        The log file is in the format specified and supplied by Swisslos, which includes multiple rounds with
        the same information about the date and players.
        Args:
            filename: file to read logs from
        Returns:
            A list of objects of type RoundLogEntry
        """
        rnds = []
        with open(filename, 'r') as file:
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
                # if we find an index, we attempt to read the date
                if index > 17:
                    datetime_string = line[0:17]
                    date = datetime.strptime(datetime_string, DATE_FORMAT)
                else:
                    date = None

                if index != -1:
                    line_json = json.loads(line[index:])
                    # read the players for those rounds
                    if 'players' in line_json:
                        players = line_json['players']
                    else:
                        players = [0, 0, 0, 0]
                    for r in line_json['rounds']:
                        if r is not None:
                            rnd_read = RoundSerializer.round_from_dict(r)
                            if rnd_read is not None:
                                nr_rounds += 1
                                rnds.append(RoundLogEntry(rnd=rnd_read, date=date, player_ids=players))
                            else:
                                nr_skipped += 1

        logging.getLogger(__name__).info('Read {} valid rounds from file'.format(nr_rounds))
        logging.getLogger(__name__).info('Skipped {} rounds'.format(nr_skipped))
        return rnds