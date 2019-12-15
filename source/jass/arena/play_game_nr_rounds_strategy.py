# HSLU
#
# Created by Thomas Koller on 05.09.18
#
import logging
from source.jass.base.const import NORTH, next_player
from source.jass.arena.play_game_strategy import PlayGameStrategy


class PlayNrRoundsStrategy(PlayGameStrategy):
    """
    Play a specific number of rounds for one game. The first dealer is always NORTH, so to make the games fair,
    the number of rounds should be a multiple of 4.
    """
    def __init__(self, nr_rounds: int):
        """
        Initialise.
        Args:
            nr_rounds: The number of rounds to play.
        """
        self._nr_rounds = nr_rounds
        self._logger = logging.getLogger(__name__)

    def play_game(self, arena) -> None:
        """
        Play a game for a number of rounds and determine the winners and points.
        Args:
            arena: the arena for which to play the game.

        """
        points_team_0 = 0
        points_team_1 = 0

        dealer = NORTH
        for nr_rounds in range(self._nr_rounds):
            arena.play_round(dealer)
            points_team_0 += arena.current_rnd.points_team_0
            points_team_1 += arena.current_rnd.points_team_1
            dealer = next_player[dealer]

        delta_points = (points_team_0 - points_team_1)

        self._logger.info('Game: Team 0: {}, Team 1: {}'.format(points_team_0, points_team_1))

        if points_team_0 > points_team_1:
            arena.add_win_team_0(delta_points)
        elif points_team_1 > points_team_0:
            arena.add_win_team_1(delta_points)
        else:
            arena.add_draw()
