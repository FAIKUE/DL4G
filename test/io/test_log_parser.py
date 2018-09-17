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

    def test_valid_cards(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        log_parser = LogParser('../resources/small_log.txt')
        rnds = log_parser.parse_rounds()

        self.assertEqual(19, len(rnds))

        for rnd in rnds:
            player_rnds = PlayerRound.all_from_complete_round(rnd)
            for i, player_rnd in enumerate(player_rnds):
                self.assertIsNotNone(player_rnd.rule)
                nr_trick, move_in_trick = divmod(i, 4)
                card_played = rnd.tricks[nr_trick, move_in_trick]
                valid_cards = player_rnd.get_valid_cards()
                card_valid = valid_cards[card_played]
                self.assertEqual(1, card_valid)


if __name__ == '__main__':
    unittest.main()