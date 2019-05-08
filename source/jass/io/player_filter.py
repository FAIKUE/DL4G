import json

from jass.base.single_player_stat import SinglePlayerStat
import pandas as pd


class PlayerFilter:
    """
    Abstract class. Used to implement filters for the Player Statistics
    """
    data = None

    def filter(self) -> [int]:
        raise NotImplementedError

    def set_data(self, data):
        self.data = data

    @staticmethod
    def _check_relative_parameter(parameter):
        if not 0 < parameter < 1:
            raise ValueError("Parameter has to be be between 0 and 1")


class PlayerStatFilter(PlayerFilter):
    def __init__(self, path_to_stat_file) -> None:
        self.stat_path = path_to_stat_file
        self._player_stats = self._read_stat()
        self._filters = []

    def add_filter(self, stat_filter: PlayerFilter):
        stat_filter.set_data(self._player_stats)
        self._filters.append(stat_filter)

    def filter(self) -> [int]:
        """
        Uses every filter added via the add_filter method
        :return: List of the filtered player ids
        """
        ids = set(self._player_stats['id'])

        for flt in self._filters:
            ids.intersection_update(flt.filter())

        return ids

    def _read_stat(self) -> pd.DataFrame:
        with open(self.stat_path) as file:
            player_stats = pd.read_json(file)

        return player_stats


class FilterMeanAbsolute(PlayerFilter):
    """
    Filters the mean points of the players with an absolute threshold
    """
    def __init__(self, bound_mean) -> None:
        super().__init__()
        self.bound_mean = bound_mean

    def filter(self) -> [int]:
        filtered = self.data[self.data['mean'] > self.bound_mean]
        return filtered['id']


class FilterStdAbsolute(PlayerFilter):
    """
    Filters the STD of the points of the players with an absolute threshold
    """
    def __init__(self, bound_std) -> None:
        super().__init__()
        self.bound_std = bound_std

    def filter(self) -> [int]:
        filtered = self.data[self.data['std'] < self.bound_std]
        return filtered['id']


class FilterPlayedGamesAbsolute(PlayerFilter):
    """
    Filters the players with the most played games based on a threshold
    """
    def __init__(self, bound_played_games) -> None:
        super().__init__()
        self.bound_played_games = bound_played_games

    def filter(self) -> [int]:
        filtered = self.data[self.data['nr'] > self.bound_played_games]
        return filtered['id']


class FilterStdRelative(PlayerFilter):
    """
    Filters players corresponding to the given quantile of the STD.
    """
    def __init__(self, rel_std) -> None:
        super().__init__()
        self.rel_std = 1 - rel_std

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_std)
        quantile = self.data['std'].quantile(self.rel_std)
        filtered = self.data[self.data['std'] < quantile]
        return filtered['id']


class FilterMeanRelative(PlayerFilter):
    """
    Filters players corresponding to the given quantile of the mean points achieved.
    """
    def __init__(self, rel_mean) -> None:
        super().__init__()
        self.rel_mean = rel_mean

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_mean)
        quantile = self.data['mean'].quantile(self.rel_mean)
        filtered = self.data[self.data['mean'] > quantile]
        return filtered['id']


class FilterPlayedGamesRelative(PlayerFilter):
    """
    Filters the players with the most played games based on a quantile
    """
    def __init__(self, rel_played_games) -> None:
        super().__init__()
        self.rel_played_games = rel_played_games

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_played_games)
        quantile = self.data['nr'].quantile(self.rel_played_games)
        filtered = self.data[self.data['nr'] > quantile]
        return filtered['id']


