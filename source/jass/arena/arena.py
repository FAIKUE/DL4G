# HSLU
#
# Created by Thomas Koller on 14.08.18
#
"""
Arena classes allow to players to compete against each other. The rules of the arenas can differ, for example to
play only a single round or to play a complete game to a specific number of points. Also the trump selection
might be carried out differently.
"""
import sys
from types import FunctionType
from typing import Callable

import numpy as np
from jass.base.const import *
from jass.base.round import Round
from jass.base.round_factory import get_round
from jass.base.player_round import PlayerRound
from jass.player.player import Player
from jass.arena.trump_selection_strategy import TrumpStrategy
from jass.arena.play_game_strategy import PlayGameStrategy


class Arena:
    """
    Class for arenas. An arena plays a number of games between two pairs of players. The number of
    games to be played can be specified. What consists of one game depends on the specific arena. The arena keeps
    statistics of the games won by each side and also of the point difference when winning.

    A game consists of at least one round of playing 36 cards.

    The class uses the strategy and template methods patterns. Most common behaviour can be modified by using the
    appropriate strategy, but there is currently no strategy to change how cards are dealt.

    """
    def __init__(self, jass_type: str,
                 trump_strategy: TrumpStrategy, play_game_strategy: PlayGameStrategy,
                 print_every_x_games: int = 5, check_move_validity=False):
        self._nr_games_to_play = 0

        # the jass type, used to get the correct round
        self._jass_type = jass_type

        # the strategies
        self._trump_strategy = trump_strategy
        self._play_game_strategy = play_game_strategy

        # the players
        self._players = [None, None, None, None]        # type: List[Player]

        # the current round that is being played
        self._rnd = None                                # type: Round

        # Statistics about the games played
        self._nr_wins_team_0 = 0                        # type: int
        self._nr_wins_team_1 = 0                        # type: int
        self._nr_draws = 0                              # type: int
        self._nr_games_played = 0                       # type: int
        self._delta_points = 0                          # type: int

        # Print  progress
        self._print_every_x_games = print_every_x_games
        self._play_card_strat: Callable[[int], None] = self._play_card_checked if \
            check_move_validity else self._play_card_unchecked

    @property
    def nr_games_to_play(self):
        return self._nr_games_to_play

    @nr_games_to_play.setter
    def nr_games_to_play(self, value):
        self._nr_games_to_play = value

    # We define properties for the individual players to set/get them easily by name
    @property
    def north(self) -> Player:
        return self._players[NORTH]

    @north.setter
    def north(self, player: Player):
        self._players[NORTH] = player

    @property
    def east(self) -> Player:
        return self._players[EAST]

    @east.setter
    def east(self, player: Player):
        self._players[EAST] = player

    @property
    def south(self) -> Player:
        return self._players[SOUTH]

    @south.setter
    def south(self, player: Player):
        self._players[SOUTH] = player

    @property
    def west(self) -> Player:
        return self._players[WEST]

    @west.setter
    def west(self, player: Player):
        self._players[WEST] = player

    @property
    def players(self):
        return self._players

    @property
    def current_rnd(self):
        return self._rnd

    # properties for the results (no setters as the values are set by the strategies using the add_win_team_x methods)
    @property
    def nr_games_played(self):
        return self._nr_games_played

    @property
    def nr_wins_team_0(self):
        return self._nr_wins_team_0

    @property
    def nr_wins_team_1(self):
        return self._nr_wins_team_1

    @property
    def nr_draws(self):
        return self._nr_draws

    @property
    def delta_points(self):
        return self._delta_points

    def get_player_round(self) -> PlayerRound:
        """
        Creates and returns an appropriate player round object to use for the players that is created from the
        current round. By default the object is a PlayerRound, but that can be overridden.

        Returns:

        """
        player_rnd = PlayerRound()
        player_rnd.set_from_round(self.current_rnd)
        return player_rnd

    def set_players(self, north: Player, east: Player, south: Player, west: Player) -> None:
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

    def add_win_team_0(self, points) -> None:
        """
        Add a win for team 0/2
        Args:
            points: number of points with which the team won
        """
        self._nr_wins_team_0 += 1
        self._delta_points += points
        self._nr_games_played += 1

    def add_win_team_1(self, points) -> None:
        """
        Add a win for team 1/3
        Args:
            points: number of points with which the team won
        """
        self._nr_wins_team_1 += 1
        self._delta_points += points
        self._nr_games_played += 1

    def add_draw(self) -> None:
        """
        Add a draw.
        """
        self._nr_draws += 1
        self._nr_games_played += 1

    def reset_stat(self) -> None:
        """
        Reset the statistics about played games.
        """
        self._nr_wins_team_0 = 0
        self._nr_wins_team_1 = 0
        self._nr_draws = 0
        self._nr_games_played = 0
        self._delta_points = 0

    def _init_round(self, dealer: int) -> None:
        """
        Initialize a new round. Should be overridden by the derived class to create the appropriate Round object
        Args:
            dealer: the dealer of the round
        """
        self._rnd = get_round(jass_type=self._jass_type, dealer=dealer)

    def deal_cards(self):
        """
        Deal cards at the beginning of a round. Default is to deal the cards randomly using the method in
        Round, but the behaviour can be overridden in a derived class.
        """
        self._rnd.deal_cards()

    def _play_card_unchecked(self, card_action: int) -> None:
        self._rnd.action_play_card(card_action)

    def _play_card_checked(self, card_action: int) -> None:
        assert card_action in np.flatnonzero(self._rnd.get_valid_cards()), "Invalid card played!"
        self._rnd.action_play_card(card_action)

    def play_round(self, dealer: int) -> None:
        """
        Play a complete round (36 cards). The results remain in self._rnd
        """
        self._init_round(dealer)
        self.deal_cards()
        self._trump_strategy.determine_trump(rnd=self._rnd, arena=self)
        player_rnd = self.get_player_round()
        for cards in range(36):
            player_rnd.set_from_round(self._rnd)
            card_action = self._players[player_rnd.player].play_card(player_rnd)
            self._play_card_strat(card_action)

    def play_game(self):
        """
        Play one game.
        """
        self._play_game_strategy.play_game(arena=self)

    def play_all_games(self):
        """
        Play the number of games.
        """
        for game_id in range(self._nr_games_to_play):
            self.play_game()
            if self.nr_games_played % self._print_every_x_games == 0:
                points_to_write = int(self.nr_games_played / self._nr_games_to_play * 40)
                spaces_to_write = 40 - points_to_write
                sys.stdout.write("\r[{}{}] {:4}/{:4} games played".format('.' * points_to_write,
                                                                          ' ' * spaces_to_write,
                                                                          self.nr_games_played,
                                                                          self._nr_games_to_play))
        sys.stdout.write('\n')

