# Copyright 2019 HSLU. All Rights Reserved.
#
# Created by Thomas Koller on 28.02.19
#
#
import json
from typing import List

from jass.base.round import Round
from jass.io.round_generator import RoundGenerator


class LogGenerator:
    """
    Create a log entry in the same format as the log file. One line of an entry consists of some header information
    followed by the rounds and player information.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.file = open(filename, 'w')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def add_rounds(self, rounds: List[Round], players: List[str]):
        rounds_dict = [RoundGenerator.generate_dict(rnd) for rnd in rounds]
        line_dict = dict(rounds=rounds_dict, players=players)
        json.dump(line_dict, self.file, separators=(',', ':'))
        self.file.write('\n')

