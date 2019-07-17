import unittest
import logging

from jass.io.log_parser_swisslos import LogParserSwisslos
from jass.io.player_round_serializer import PlayerRoundSerializer
from jass.base.player_round import PlayerRound

TEST_FILE = '../resources/small_log.txt'


class PlayerRoundSerializerTestCase(unittest.TestCase):
    def test_from_and_to_dict(self):
        # read rounds
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        rnd_log_entries = LogParserSwisslos.parse_rounds(TEST_FILE)

        for entry in rnd_log_entries:
            rnd = entry.rnd
            player_rounds = PlayerRound.all_from_complete_round(rnd)

            for player_round in player_rounds:
                # Generate and reconstruct player round
                player_round_dict = PlayerRoundSerializer.player_round_to_dict(player_round)
                self.assertIsNotNone(player_round_dict)

                player_round_from_dict = PlayerRoundSerializer.player_round_from_dict(player_round_dict)
                self.assertIsNotNone(player_round_from_dict)

                player_round_from_dict.assert_invariants()

                if player_round_from_dict != player_round:
                    print('Orig:')
                    print(player_round)
                    print('Restored:')
                    print(player_round_from_dict)
                    print('Dict:')
                    print(player_round_dict)

                # reconstructed round should be the same
                self.assertTrue(player_round_from_dict == player_round)


if __name__ == '__main__':
    unittest.main()
