# HSLU
#
# Created by Thomas Koller on 24.08.18
#

from jass.base.game import Game
from jass.io.round_generator import RoundGenerator
class GameGenerator:
    """
    Class for generation of the dict/json representation of a game (Game)
    """
    @staticmethod
    def generate_dict(game: Game) -> dict:
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
        data['winner'] = game.winner
        data['points_team0'] = int(game.points_team0)
        data['points_team1'] = int(game.points_team1)
        data['time_started'] = game.time_started
        data['time_finished'] = game.time_finished

        rounds = []
        for i in range(game.nr_rounds):
            round_data = RoundGenerator.generate_dict(game.round[i])
            rounds.append(round_data)
        data['rounds'] = rounds

        return data
