# HSLU
#
# Created by Thomas Koller on 24.08.18
#

from jass.base.game import Game
from jass.io.round_serializer import RoundSerializer


class GameSerializer:
    """
    Class for generation of the dict/json representation of a game (Game) and vice
    versa.
    """
    @staticmethod
    def game_to_dict(game: Game) -> dict:
        """
        Generate dict for the game that corresponds to the json description. RoundGenerator is used to generate
        the rounds for the game.

        Args:
            game: the game to convert

        Returns:
            dict representation of the game that can be converted to json
        """
        data = dict()
        data['north'] = game.north
        data['east'] = game.east
        data['south'] = game.south
        data['west'] = game.west
        data['northUrl'] = game.north_url
        data['eastUrl'] = game.east_url
        data['southUrl'] = game.south_url
        data['westUrl'] = game.west_url
        data['northId'] = game.north_id
        data['eastId'] = game.east_id
        data['southId'] = game.south_id
        data['westId'] = game.west_id
        data['winner'] = game.winner
        data['pointsTeam0'] = int(game.points_team0)
        data['pointsTeam1'] = int(game.points_team1)
        data['timeStarted'] = game.time_started
        data['timeFinished'] = game.time_finished

        if game.errors:
            data['errors'] = game.errors

        rounds = []
        for i in range(game.nr_rounds):
            round_data = RoundSerializer.round_to_dict(game.round[i])
            rounds.append(round_data)
        data['rounds'] = rounds

        return data

    @staticmethod
    def dict_to_game(data: dict) -> Game or None:
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

        if 'errors' in data:
            game._errors = data['errors']

        rounds = data['rounds']
        # use temporary list for rounds (as Game.add_entry changes the points)
        rnds = []

        for round_data in rounds:
            rnd = RoundSerializer.round_from_dict(round_data)
            rnds.append(rnd)

        game._rounds = rnds
        return game
