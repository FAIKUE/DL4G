# HSLU
#
# Created by Thomas Koller on 10.07.19
#
import datetime
from typing import List
from jass.base.round import Round



class RoundLogEntry:
    """
    Class to capture the information contained in the log entries (and other possible other files and
    not always in the same format).

    It contains the actual round and additional information, which is currently the time stamp of the
    entry and the players playing the round.

    (The information here was previously stores using dicts, but an explicit class seems better for
    understanding the code)

    """
    def __init__(self, rnd: Round, date: datetime.datetime = None, players: List[int] = None):
        self.rnd = rnd
        self.date = date
        self.players = players
