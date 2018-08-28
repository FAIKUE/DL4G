# HSLU
#
# Created by Thomas Koller on 15.08.18
#

from jass.base.const import *
from jass.arena.arena import Arena


class ArenaNrRounds(Arena):
    """
    Arena that plays a specific number of rounds for a game. The default is 4, but the number can be changed.
    """

    def __init__(self):
        super(ArenaNrRounds, self).__init__()
        self._nr_rounds_in_game = 4

    @property
    def nr_rounds_in_game(self):
        return self._nr_rounds_in_game

    @nr_rounds_in_game.setter
    def nr_rounds_in_game(self, value):
        self._nr_rounds_in_game = value

    def play_game(self) -> None:
        """
        Play the indicated number of rounds.

        """
        points_team_0 = 0
        points_team_1 = 0

        dealer = NORTH
        for nr_rounds in range(self.nr_rounds_in_game):
            self.play_round(dealer)
            points_team_0 += self._rnd.points_team_0
            points_team_1 += self._rnd.points_team_1
            dealer = next_player[dealer]

        self._nr_games_played += 1
        self._delta_points += (points_team_0 - points_team_1)

        if points_team_0 > points_team_1:
            self._nr_wins_team_0 += 1
        elif points_team_1 > points_team_0:
            self._nr_wins_team_1 += 1
        else:
            self._nr_draws += 1