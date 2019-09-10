# HSLU
#
# Created by Thomas Koller on 10.07.19
#
import datetime
from typing import List

from jass.base.label_play import LabelPlay
from jass.base.label_trump import LabelTrump
from jass.base.player_round import PlayerRound
from jass.base.player_round_cheating import PlayerRoundCheating
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
    def __init__(self, rnd: Round, date: datetime.datetime = None, player_ids: List[int] = None):
        self.rnd = rnd
        self.date = date
        self.player_ids = player_ids


class PlayerRoundLogEntry:
    """
    Class to capture the information stored in a entry for a player round. It includes additional information
    that might be necessary for training or for statistical data.
    """
    def __init__(self, player_rnd: PlayerRound,
                 date: datetime.datetime = None,
                 player_id: int = None,
                 label: LabelPlay = None):
        self.player_rnd = player_rnd
        self.date = date
        self.player_id = player_id
        self.label = label


class PlayerRoundCheatingLogEntry:
    """
    Class to capture the information stored in a entry for a player round. It includes additional information
    that might be necessary for training or for statistical data.
    """
    def __init__(self, player_rnd_cheating: PlayerRoundCheating, date: datetime.datetime = None, player_id: int = None):
        self.player_rnd_cheating = player_rnd_cheating
        self.date = date
        self.player_id = player_id


class PlayerRoundTrumpLogEntry:
    """
    Class to capture the information stored in a entry for a player round for trump actions.
    """
    def __init__(self, player_rnd: PlayerRound,
                 date: datetime.datetime = None,
                 player_id: int = None,
                 label: LabelTrump = None):
        self.player_rnd = player_rnd
        self.date = date
        self.player_id = player_id
        self.label = label
