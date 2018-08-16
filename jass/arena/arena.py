# HSLU
#
# Created by Thomas Koller on 14.08.18
#
"""
Arena classes allow to players to compete against each other. The rules of the arenas can differ, for example to
play only a single round or to play a complete game to a specific number of points. Also the trump selection
might be carried out differently.
"""
from jass.base.const import *
from jass.base.round import Round
from jass.base.player_round import PlayerRound
from jass.player.player import Player


class Arena:
    """
    Abstract base class for arenas. An arena plays a number of games between two pairs of players. The number of
    games to be played can be specified. What consists of one game depends on the specific arena. The arena keeps
    statistics of the games won by each side and also of the point difference when winning.

    A game consists of at least one round of playing 36 cards.

    The class uses the template method patters, the minimal method that must be overridden is play_game, that
    plays some rounds, determines the winner and updates the statistics.

    Optionally the methods declare_trump and deal_cards can be overridden for special behaviour.
    """
    def __init__(self):
        self._nr_games_to_play = 0

        # the players
        self._players: List[Player] = [None, None, None, None]

        # the current round that is being played
        self._rnd: Round = None

        # Statistics about the games played
        self._nr_wins_team_0: int = 0
        self._nr_wins_team_1: int = 0
        self._nr_draws: int = 0
        self._nr_games_played: int = 0
        self._delta_points: int = 0

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

    # properties for the results (no setters as the values are set by the class or subclass)
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

    def _init_round(self, dealer: int) -> None:
        """
        Initialize a new round.
        Args:
            dealer: the dealer of the round
        """
        self._rnd = Round(dealer)


    def deal_cards(self):
        """
        Deal cards at the beginning of a round. Default is to deal the cards randomly using the method in
        Round, but the behaviour can be overridden in a derived class.
        """
        self._rnd.deal_cards()

    def _determine_trump_from_players(self) -> None:
        """
        Determine trump through the players. The round must have been dealt, and the dealer assigned.
        """
        player_rnd = PlayerRound()
        player_rnd.set_from_round(self._rnd)

        # ask first player
        trump_action = self._players[player_rnd.player].select_trump(player_rnd)
        self._rnd.action_trump(trump_action)

        if trump_action == PUSH:
            # ask second player
            player_rnd.set_from_round(self._rnd)
            trump_action = self._players[player_rnd.player].select_trump(player_rnd)
            self._rnd.action_trump(trump_action)

    def determine_trump(self) -> None:
        """
        Determine the trump. The default is to determine the trump from the players, but the method can be
        overridden in a derived class for a different behaviour
        """
        self._determine_trump_from_players()

    def play_round(self, dealer: int) -> None:
        """
        Play a complete round (36 cards). The results remain in self._rnd
        """
        self._init_round(dealer)
        self.deal_cards()
        self.determine_trump()

        player_rnd = PlayerRound()
        for cards in range(36):
            player_rnd.set_from_round(self._rnd)
            card_action = self._players[player_rnd.player].play_card(player_rnd)
            self._rnd.action_play_card(card_action)

    def play_game(self) -> None:
        """
        Play a game and determine the winners and points. Must be overridden in derived class

        """
        pass

    def play_all_games(self):
        """
        Play the number of games.
        """
        for game_id in range(self._nr_games_to_play):
            self.play_game()
