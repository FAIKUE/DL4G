# HSLU
#
# Created by Thomas Koller on 24.08.18
#

from jass.base.game import Game
from jass.io.round_parser import RoundParser


class GameParser:
    """
    Class to parse a Game from dict/json
    """
    @staticmethod
    def parse_game(data: dict) -> Game or None:
        """
        Parse a dict to reconstruct a Game
        Args:
            data: dict containing the game data

        Returns:
            the game
        """
        game = Game()
        game.set_players(data['north'], data['east'], data['south'], data['west'])
        game.winner = data['winner']
        game._points_team0 = data['pointsTeam0']
        game._points_team1 = data['pointsTeam1']
        game.time_started = data['timeStarted']
        game.time_finished = data['timeFinished']

        rounds = data['rounds']
        # use temporary list for rounds (as Game.add_entry changes the points)
        rnds = []

        for round_data in rounds:
            rnd = RoundParser.parse_round(round_data)
            rnds.append(rnd)

        game._rounds = rnds
        return game
