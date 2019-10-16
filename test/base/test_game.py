import unittest
import json
import datetime

from jass.base.game import Game
from jass.ion.log_parser_swisslos import LogParserSwisslos
from jass.ion.game_serializer import GameSerializer
from jass.ion.round_serializer import RoundSerializer


class GameTestCase(unittest.TestCase):
    def test_game(self):
        round_string = '{"trump":5,"dealer":3,"tss":1,"tricks":[' \
                       '{"cards":["C7","CK","C6","CJ"],"points":17,"win":0,"first":2},' \
                       '{"cards":["S7","SJ","SA","C10"],"points":12,"win":0,"first":0},' \
                       '{"cards":["S9","S6","SQ","D10"],"points":24,"win":3,"first":0},' \
                       '{"cards":["H10","HJ","H6","HQ"],"points":26,"win":1,"first":3},' \
                       '{"cards":["H7","DA","H8","C9"],"points":8,"win":1,"first":1},' \
                       '{"cards":["H9","CA","HA","DJ"],"points":2,"win":1,"first":1},' \
                       '{"cards":["HK","S8","SK","CQ"],"points":19,"win":1,"first":1},' \
                       '{"cards":["DQ","D6","D9","DK"],"points":18,"win":0,"first":1},' \
                       '{"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}],' \
                       '"player":[{"hand":[]},{"hand":[]},{"hand":[]},{"hand":[]}],"jassTyp":"SCHIEBER_2500"}'
        round_dict = json.loads(round_string)
        rnd = RoundSerializer.round_from_dict(round_dict)

        game = Game()
        game.set_players('north', 'east', 'south', 'west')
        self.assertEqual('north', game.north)
        self.assertEqual('east', game.east)
        self.assertEqual('south', game.south)
        self.assertEqual('west', game.west)

        game.time_started = datetime.datetime.now()

        game.add_round(rnd)
        self.assertEqual(1, game.nr_rounds)

        game.add_round(rnd)
        self.assertEqual(2, game.nr_rounds)

        game.time_finished = datetime.datetime.now()

        game.winner = 1

        # test __eq__
        self.assertTrue(game == game)

    def test_parser_generator(self):
        round_string = '{"trump":5,"dealer":3,"tss":1,"tricks":[' \
                       '{"cards":["C7","CK","C6","CJ"],"points":17,"win":0,"first":2},' \
                       '{"cards":["S7","SJ","SA","C10"],"points":12,"win":0,"first":0},' \
                       '{"cards":["S9","S6","SQ","D10"],"points":24,"win":3,"first":0},' \
                       '{"cards":["H10","HJ","H6","HQ"],"points":26,"win":1,"first":3},' \
                       '{"cards":["H7","DA","H8","C9"],"points":8,"win":1,"first":1},' \
                       '{"cards":["H9","CA","HA","DJ"],"points":2,"win":1,"first":1},' \
                       '{"cards":["HK","S8","SK","CQ"],"points":19,"win":1,"first":1},' \
                       '{"cards":["DQ","D6","D9","DK"],"points":18,"win":0,"first":1},' \
                       '{"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}],' \
                       '"player":[{"hand":[]},{"hand":[]},{"hand":[]},{"hand":[]}],"jassTyp":"SCHIEBER_2500"}'
        round_dict = json.loads(round_string)
        rnd = RoundSerializer.round_from_dict(round_dict)

        game = Game()
        game.set_players('north', 'east', 'south', 'west')
        game.add_round(rnd)
        game.add_round(rnd)
        game.winner = 0
        data = GameSerializer.game_to_dict(game)
        game_restored = GameSerializer.dict_to_game(data)

        self.assertTrue(game, game_restored)


if __name__ == '__main__':
    unittest.main()
