import unittest
import json
from jass.base.player_round import PlayerRound
from jass.io.log_parser import LogParser
from jass.player_service.request_generator import PlayerRoundRequestGenerator
from jass.player_service.request_parser import PlayerRoundParser


class PlayerRoundGeneratorTestCase(unittest.TestCase):
    def test_generator(self):
        # load some data to use for the tests
        log_parser = LogParser('../resources/small_log.txt')
        rnd_entries = log_parser.parse_rounds()
        for rnd_entry in rnd_entries:
            player_rnds = PlayerRound.all_from_complete_round(rnd_entry.rnd)
            for player_rnd in player_rnds:
                json_data = PlayerRoundRequestGenerator.generate_json(player_rnd)
                # in the service, we directly get the json dict
                json_dict = json.loads(json_data)
                parser = PlayerRoundParser(json_dict)
                is_valid = parser.is_valid_request()
                self.assertTrue(is_valid)
                self.assertTrue(player_rnd == parser.get_parsed_round())


if __name__ == '__main__':
    unittest.main()
