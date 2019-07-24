import json
import numpy as np
import logging


class PlayerStat:
    """
    Class to contain the player information (instead of using dict directly)
    """
    def __init__(self, id: int, mean: float, std:float, nr: int):
        self.id = id
        self.mean = mean
        self.std = std
        self.nr = nr


class PlayerIdFilter:
    """
    Abstract class. Used to implement filters for the Player Statistics
    """

    def __init__(self):
        self.player_stats = None

    def filter(self) -> [int]:
        raise NotImplementedError

    def set_data(self, player_stat: [PlayerStat]):
        # (renamed from data)
        self.player_stats = player_stat

    @staticmethod
    def _check_relative_parameter(parameter):
        if not 0 < parameter < 1:
            raise ValueError("Parameter has to be be between 0 and 1")


class PlayerStatFilter(PlayerIdFilter):
    def __init__(self, path_to_stat_file) -> None:
        self.stat_path = path_to_stat_file
        self._player_stats = self._read_stat()
        self._filters = []

    def add_filter(self, stat_filter: PlayerIdFilter):
        stat_filter.set_data(self._player_stats)
        self._filters.append(stat_filter)

    def filter(self) -> [int]:
        """
        Uses every filter added via the add_filter method
        :return: List of the filtered player ids
        """
        #ids = set(self._player_stats['id'])
        ids = set([p.id for p in self._player_stats])
        print("Players before filter: " + str(len(ids)))
        for i, flt in enumerate(self._filters):
            ids.intersection_update(flt.filter())
            print("Players after " + str(i + 1) + " filter(s): " + str(len(ids)))

        return ids

    def _read_stat(self) -> [PlayerStat]:
        with open(self.stat_path) as file:
            data = json.load(file)
        return [PlayerStat(id=el['id'], mean=el['mean'], std=el['std'], nr=el['nr']) for el in data]


class FilterMeanAbsolute(PlayerIdFilter):
    """
    Filters the mean points of the players with an absolute threshold
    """
    def __init__(self, bound_mean) -> None:
        super().__init__()
        self.bound_mean = bound_mean

    def filter(self) -> [int]:
        filtered = [p.id for p in self.player_stats if p.mean > self.bound_mean]
        return filtered


class FilterStdAbsolute(PlayerIdFilter):
    """
    Filters the STD of the points of the players with an absolute threshold
    """
    def __init__(self, bound_std) -> None:
        super().__init__()
        self.bound_std = bound_std

    def filter(self) -> [int]:
        filtered = [p.id for p in self.player_stats if p.std < self.bound_std]
        return filtered


class FilterPlayedGamesAbsolute(PlayerIdFilter):
    """
    Filters the players with the most played games based on a threshold
    """
    def __init__(self, bound_played_games) -> None:
        super().__init__()
        self.bound_played_games = bound_played_games

    def filter(self) -> [int]:
        filtered = [p.id for p in self.player_stats if p.nr > self.bound_played_games]
        return filtered


class FilterStdRelative(PlayerIdFilter):
    """
    Filters players corresponding to the given quantile of the STD.
    """
    def __init__(self, rel_std) -> None:
        super().__init__()
        self.rel_std = 1 - rel_std

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_std)
        #quantile = self.player_stats['std'].quantile(self.rel_std)
        std_data = [p.std for p in self.player_stats]
        quantile = np.quantile(std_data, self.rel_std)
        print('Quantile calculated for relative std: {}'.format(quantile))
        filtered = [p.id for p in self.player_stats if p.std < quantile]
        return filtered


class FilterMeanRelative(PlayerIdFilter):
    """
    Filters players corresponding to the given quantile of the mean points achieved.
    """
    def __init__(self, rel_mean) -> None:
        super().__init__()
        self.rel_mean = rel_mean

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_mean)
        mean_data = [p.mean for p in self.player_stats]
        quantile = np.quantile(mean_data, self.rel_mean)
        print('Quantile calculated for relative mean: {}'.format(quantile))
        filtered = [p.id for p in self.player_stats if p.mean > quantile]
        return filtered


class FilterPlayedGamesRelative(PlayerIdFilter):
    """
    Filters the players with the most played games based on a quantile
    """
    def __init__(self, rel_played_games) -> None:
        super().__init__()
        self.rel_played_games = rel_played_games

    def filter(self) -> [int]:
        self._check_relative_parameter(self.rel_played_games)

        nr_data = [p.nr for p in self.player_stats]
        quantile = np.quantile(nr_data, self.rel_played_games)
        print('Quantile calculated for relative played games: {}'.format(quantile))
        filtered = [p.id for p in self.player_stats if p.nr > quantile]
        return filtered

