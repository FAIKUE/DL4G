# HSLU
#
# Created by Thomas Koller on 15.08.18
#

import random
from jass.base.const import *
from jass.arena.arena import Arena


class ArenaRandomTrump(Arena):
    """
    Arena that selects the trump randomly and then plays four rounds for a game.
    """

    def determine_trump(self) -> None:
        """
        Overridden to determine a trump randomly and select forehand randomly.
        """
        # select randomly to push or not
        if random.randrange(2) == 1:
            self._rnd.action_trump(PUSH)

        # select random trump
        trump = random.randint(0, MAX_TRUMP)
        self._rnd.action_trump(trump)

    def play_game(self) -> None:
        """
        Play four rounds, as even with random trump, there might be a slight advantage of playing first, so
        each player gets to be dealer once.

        """
        points_team_0 = 0
        points_team_1 = 0

        for dealer in range(4):
            self.play_round(dealer)
            points_team_0 += self._rnd.points_team_0
            points_team_1 += self._rnd.points_team_1

        self._nr_games_played += 1
        self._delta_points += (points_team_0 - points_team_1)

        if points_team_0 > points_team_1:
            self._nr_wins_team_0 += 1
        elif points_team_1 > points_team_0:
            self._nr_wins_team_1 += 1
        else:
            self._nr_draws += 1
