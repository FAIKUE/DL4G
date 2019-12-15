# HSLU
#
# Created by Thomas Koller on 24.08.18
#
from source.jass.base.const import *
from source.jass.base.round import Round


class Game:
    """
    A game consists of a number of (full) rounds that are played between 4 players.

    (Most of the logic and the available data is based on Rounds. The game is primarily used to store and load
    games that are played on the server. For that reason it is now extended to support the urls of the players
    and error that occurred while playing.
    """

    def __init__(self):
        self._players = ['', '', '', '']                # type: [str]
        self._urls = ['', '', '', '']                   # type: [str]
        self._player_ids = ['', '', '', '']             # type: [str]
        self._rounds = []                               # type: [Round]
        self._points_team0 = 0                          # type: int
        self._points_team1 = 0                          # type: int
        self._winner = -1                               # type: int

        # time is not set by default, as the game can also be created by reading from db
        self._time_started = None
        self._time_finished = None

        # errors will be a list of str messages about possible errors while playing a game on the server
        # such as timeout or connection problems
        self._errors = []

    def __eq__(self, other: 'Game'):
        """
        Compare two instances. Useful for tests when the representations are encoded and decoded. The objects are
        considered equal if they have the same properties. As the rounds contain  numpy arrays, we can not compare
        dict directly.
        Args:
            other: the other object to compare to.

        Returns:
            True if the objects are the same.
        """
        result = \
            self._players == other._players and \
            self.points_team0 == other.points_team0 and \
            self.points_team1 == other.points_team1 and \
            self.time_started == other.time_started and \
            self.time_finished == other.time_finished and \
            self.errors == other.errors

        if not result:
            return False

        for i in range(self.nr_rounds):
            if not self._rounds[i] == other._rounds[i]:
                return False

        return True

    # Read only properties
    @property
    def points_team0(self) -> int:
        return self._points_team0

    @property
    def points_team1(self) -> int:
        return self._points_team1

    @property
    def round(self) -> [Round]:
        return self._rounds

    @property
    def errors(self) -> [str]:
        return self._errors

    # Derived properties
    @property
    def nr_rounds(self) -> int:
        return len(self._rounds)

    # Read / Write properties
    @property
    def north(self) -> str:
        return self._players[NORTH]

    @north.setter
    def north(self, player: str):
        self._players[NORTH] = player

    @property
    def east(self) -> str:
        return self._players[EAST]

    @east.setter
    def east(self, player: str):
        self._players[EAST] = player

    @property
    def south(self) -> str:
        return self._players[SOUTH]

    @south.setter
    def south(self, player: str):
        self._players[SOUTH] = player

    @property
    def west(self) -> str:
        return self._players[WEST]

    @west.setter
    def west(self, player: str):
        self._players[WEST] = player

    @property
    def north_url(self) -> str:
        return self._urls[NORTH]

    @north_url.setter
    def north_url(self, url: str):
        self._urls[NORTH] = url

    @property
    def east_url(self) -> str:
        return self._urls[EAST]

    @east_url.setter
    def east_url(self, url: str):
        self._urls[EAST] = url

    @property
    def south_url(self) -> str:
        return self._urls[SOUTH]

    @south_url.setter
    def south_url(self, url: str):
        self._urls[SOUTH] = url

    @property
    def west_url(self) -> str:
        return self._urls[WEST]

    @west_url.setter
    def west_url(self, url: str):
        self._urls[WEST] = url

    @property
    def north_id(self):
        return self._player_ids[NORTH]

    @property
    def east_id(self):
        return self._player_ids[EAST]

    @property
    def south_id(self):
        return self._player_ids[SOUTH]

    @property
    def west_id(self):
        return self._player_ids[WEST]

    @property
    def winner(self) -> int:
        return self._winner

    @winner.setter
    def winner(self, value: int):
        self._winner = value

    @property
    def time_started(self):
        return self._time_started

    @time_started.setter
    def time_started(self, value):
        self._time_started = value

    @property
    def time_finished(self):
        return self._time_finished

    @time_finished.setter
    def time_finished(self, value):
        self._time_finished = value

    def set_players(self, north: str, east: str, south: str, west: str) -> None:
        """
        Set the players.
        Args:
            north: North player
            east: East player
            south: South player
            west: West player
        """
        self._players[NORTH] = north
        self._players[EAST] = east
        self._players[SOUTH] = south
        self._players[WEST] = west

    def set_urls(self, north_url: str, east_url: str, south_url: str, west_url: str) -> None:
        """
        Set the players.
        Args:
           north_url: url of north player
           east_url: url of east player
           south_url: url of south player
           west_url: url of west player
        """
        self._urls[NORTH] = north_url
        self._urls[EAST] = east_url
        self._urls[SOUTH] = south_url
        self._urls[WEST] = west_url

    def set_player_ids(self, north_id: str, east_id: str, south_id: str, west_id: str) -> None:
        """
        Set the players.
        Args:
           north_id: id of north player
           east_id: id of east player
           south_id: id of south player
           west_id: id of west player
        """
        self._player_ids[NORTH] = north_id
        self._player_ids[EAST] = east_id
        self._player_ids[SOUTH] = south_id
        self._player_ids[WEST] = west_id

    def add_round(self, rnd: Round) -> None:
        """
        Add a round to the game. The points are adjusted from the round.
        Args:
            rnd: The Round to add

        """
        self._rounds.append(rnd)
        self._points_team0 += rnd.points_team_0
        self._points_team1 += rnd.points_team_1

    def add_error(self, error: str) -> None:
        """
        Add an error message.
        Args:
            error: Error message to add
        """
        self._errors.append(error)
