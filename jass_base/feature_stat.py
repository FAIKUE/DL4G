# HSLU
#
# Created by Thomas Koller on 22.01.18
#
"""
Methods for evaluating the card play algorithm.
"""

from typing import Dict

import numpy as np


class FeatureStat:
    """
        Generic statistic interface that allows to calculate properties using the input features, the given label and
        the evaluated result. The class should be useful for different features.
    """

    def __init__(self):
        self.description = 'base class'
        pass


    def add_result(self, features: np.ndarray, label: int, result: int):
        """
        Add one result from the features, label and the result

        Args:
            features: the input features
            label: the input label (i.e. expected result)
            result: the actual result calculated from the network
        """
        pass


    def get(self) -> Dict:
        """
            Get the results of the statistics as a dictionary. The values of the result depend on the statistics.
        Returns:
            dictionary with results
        """
        pass


class FeatureStatCollection:
    """
    Collection of feature stats that will be calculated.
    """

    def __init__(self):
        self.stat = []


    def add_statistic(self, statistic: FeatureStat):
        self.stat.append(statistic)

    def add_result(self, features: np.ndarray, label: int, result: int):
        """
        Add result for every feature statistics in the collection

        Args:
            features:
            label:
            result:
        """
        for s in self.stat:
            s.add_result(features, label, result)

    def get(self) -> Dict:
        result = {}
        for s in self.stat:
            result[s.description] = s.get()
        return result


class AccuracyByMoveStat(FeatureStat):
    """
    Calculate the accuracy by move number
    """

    def __init__(self):
        super().__init__()
        self.description = 'Accuracy by move number'
        self.positives_by_move = np.zeros(36, np.int64)
        self.count_by_move = np.zeros(36, np.int64)


    def add_result(self, features: np.ndarray, label: int, result: int):
        nr_tricks_played = features[231]
        nr_cards = features[234]
        move = (int)(nr_tricks_played * 4 + nr_cards)
        self.count_by_move[move] += 1
        if label == result:
            self.positives_by_move[move] += 1


    def get(self):
        return {
            'count': self.count_by_move,
            'raw': self.positives_by_move,
            'accuracy': self.positives_by_move / self.count_by_move
        }