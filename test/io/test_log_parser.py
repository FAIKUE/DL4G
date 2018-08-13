import unittest
import logging
from jass.io.log_parser import LogParser
from jass.base.player_round import PlayerRound


class LogParserTestCase(unittest.TestCase):

    def test_log_parser(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        log_parser = LogParser('../resources/small_log.txt')
        rnds = log_parser.parse_rounds()

        self.assertEqual(19, len(rnds))

        # 1+2+3+...+35 = 35 * (35+1)/2
        sum_of_all_cards = 35*18
        for rnd in rnds:
            # some basic tests if the rnds are valid
            rnd.assert_invariants()
            self.assertEqual(36, rnd.nr_played_cards)
            self.assertEqual(9, rnd.nr_tricks)
            self.assertEqual(sum_of_all_cards, rnd.tricks.sum(axis=None))

            # test player_rounds on the same data
            player_rnds = PlayerRound.all_from_complete_round(rnd)
            for player_rnd in player_rnds:
                player_rnd.assert_invariants()



if __name__ == '__main__':
    unittest.main()
