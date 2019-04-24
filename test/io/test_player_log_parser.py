import unittest

from jass.io.player_round_log_parser import PlayerRoundLogParser


class PlayerRoundLogGeneratorCase(unittest.TestCase):

    def test_file_can_be_loaded(self):
        testee = PlayerRoundLogParser()
        result = testee.parse_rounds_from_file("..\\resources\\small_player_log.txt")
        self.assertTrue(len(result) == 11)

    def test_parsing(self):
        testee = PlayerRoundLogParser()
        result = testee.parse_rounds_from_file("..\\resources\\small_player_log.txt")
        single_player_round = result[0]

        self.assertEqual(5, single_player_round.trump)
        self.assertEqual(1, single_player_round.declared_trump)
        self.assertListEqual([2, -1, -1, -1], single_player_round.current_trick.tolist())
        self.assertEqual(29, single_player_round.nr_played_cards)
        self.assertEqual(0, single_player_round.dealer)
        self.assertEqual(1, single_player_round.player)
        self.assertEqual(False, single_player_round.forehand)

        self.assertEqual(7, single_player_round.nr_tricks)
        self.assertEqual(1, single_player_round.nr_cards_in_trick)

        expected_hand = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

        self.assertListEqual(expected_hand, single_player_round.hand.tolist())

    def test_consistency(self):
        testee = PlayerRoundLogParser()
        result = testee.parse_rounds_from_file("..\\resources\\small_player_log.txt")
        for rnd in result:
            rnd.assert_invariants()

    def test_cheating_consistency(self):
        testee = PlayerRoundLogParser()
        result = testee.parse_cheating_rounds_from_file("..\\resources\\small_cheating_player_log.txt")
        for rnd in result:
            rnd.assert_invariants()

if __name__ == '__main__':
    unittest.main()
