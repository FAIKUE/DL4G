# HSLU
#
# Created by Thomas Koller on 04.10.18
#
import numpy as np
from typing import Dict
from jass.base.player_round import PlayerRound


class PlayerStat:
    """
        Generic statistic interface that allows to calculate properties using the round, the given label and
        the result (played card or other low level result like probabilities) obtained from a player.
    """

    def __init__(self):
        self.description = 'Base Stat'
        pass

    def add_result_for_action(self, label: int, action: int, player_rnd: PlayerRound = None):
        """
        Add one result from label and the action.

        Args:
            label: the input label (i.e. expected action for example from test data)
            action: the actual result calculated from the network
            player_rnd: the player rnd at the moment of the action, can be used to derive extra information for
            the statistics (what move, what trump, etc.)
        """
        raise NotImplementedError

    def get(self) -> Dict:
        """
            Get the results of the statistics as a dictionary. The values of the result depend on the statistics.
        Returns:
            dictionary with results
        """
        raise NotImplementedError


class PlayerStatCollection:
    """
    Collection of feature stats that will be calculated.
    """

    def __init__(self):
        self.stat = []

    def add_statistic(self, statistic: PlayerStat):
        self.stat.append(statistic)

    def add_result_for_action(self, label: int, action: int, player_rnd: PlayerRound = None):
        """
        Add result for every feature statistics in the collection

        Args:
            label: the input label (i.e. expected action for example from test data)
            action: the actual result calculated from the network
            player_rnd: the player rnd at the moment of the action, can be used to derive extra information for
            the statistics (what move, what trump, etc.)
        """
        for s in self.stat:
            s.add_result_for_action(label, action, player_rnd)

    def get(self) -> Dict:
        result = {}
        for s in self.stat:
            result[s.description] = s.get()
        return result


class AccuracyByMoveStat(PlayerStat):
    """
    Calculate the accuracy by move number
    """
    def __init__(self):
        super().__init__()
        self.description = 'Accuracy by move number'
        self.positives_by_move = np.zeros(36, np.int64)
        self.count_by_move = np.zeros(36, np.int64)

    def add_result_for_action(self, label: int, action: int, player_rnd: PlayerRound = None):
        move = int(player_rnd.nr_played_cards)
        self.count_by_move[move] += 1
        if label == action:
            self.positives_by_move[move] += 1

    def get(self):
        return {
            'count': self.count_by_move.tolist(),
            'raw': self.positives_by_move.tolist(),
            'accuracy': (self.positives_by_move / self.count_by_move).tolist()
        }
