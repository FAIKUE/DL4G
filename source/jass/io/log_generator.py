# Copyright 2019 HSLU. All Rights Reserved.
#
# Created by Thomas Koller on 28.02.19
#
#
import json
import datetime
import random
from typing import List

from jass.base.round import Round
from jass.io.round_generator import RoundSerializer


class LogGenerator:
    """
    Create a log entry in a similar format as the original log file, but with the following changes:
    - date and player information are inside the json for each round
    - there is one round on each line formatted as one json dict

    A line from the file can be parsed usind Round_Parser.parse_round_all
    """

    def __init__(self, basename: str, max_entries: int, max_buffer=10000):
        self._basename = basename
        self._extension = '.txt'
        self._max_entries = max_entries
        self._max_buffer = max_buffer
        self._current_file_number = 0
        self._nr_lines_in_file = 0

        self._file = None
        self._buffer = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if len(self._buffer) > 0:
            self._write_buffer()
        if self._file is not None:
            self._file.close()

    def _open_new_file(self):
        if self._file is not None:
            self._file.close()
        self._current_file_number += 1
        filename = self._basename + '{:02d}'.format(self._current_file_number) + self._extension
        print(filename)
        self._file = open(filename, mode='w')
        self._nr_lines_in_file = 0

    def _write_buffer(self):
        random.shuffle(self._buffer)
        for line in self._buffer:
            if self._nr_lines_in_file >= self._max_entries or self._file is None:
                self._open_new_file()

            self._file.write(line)
            self._file.write('\n')
            self._nr_lines_in_file += 1
        self._buffer.clear()

    def add_round(self, rnd: Round, players: List[str], date: datetime.datetime):
        date_string = date.strftime('%d.%m.%y %H:%M:%S')
        rounds_dict = RoundSerializer.generate_dict_all(rnd, date_string, players)
        line = json.dumps(rounds_dict, separators=(',', ':'))
        self._buffer.append(line)
        if len(self._buffer) > self._max_buffer:
            self._write_buffer()
