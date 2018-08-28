import unittest

import jass_base.game
from jass_base.game import *


class GameTestCase(unittest.TestCase):
    def test_card_table(self):
        values = jass_base.game.card_values
        # make sure all rows sum up to 152
        sums = np.sum(values, 1)
        for i in range(6):
            self.assertEqual(152, sums[i])

    def test_tricks(self):
        trick = Trick()
        trick.cards = np.array([SA, SK, SQ, SJ])
        cards_enc = trick.get_cards_enc()
        for i in range(36):
            expected = 0
            if i == jass_base.game.SA or i == jass_base.game.SK or i == jass_base.game.SQ or i == jass_base.game.SJ:
                expected = 1
            self.assertEqual(expected, cards_enc[i])

    def test_calculate_points_in_tricks(self):
        trick = Trick()
        trick.cards = np.array([SA, SK, SQ, SJ])
        trick.calc_points(trump=0)
        self.assertEqual(20, trick.points)

        trick.calc_points(1)
        self.assertEqual(20, trick.points)

        trick.calc_points(2)
        self.assertEqual(38, trick.points)

        trick.calc_points(3)
        self.assertEqual(20, trick.points)

    def test_tricks_encode_player(self):
        trick = Trick()
        trick.cards = np.array([SA, SK, HQ, C7])
        trick.first_player = 0
        hands = trick.get_cards_enc_player()
        self.assertEqual(4, np.sum(hands))
        self.assertEqual(1, hands[0, SA])
        self.assertEqual(1, hands[3, SK])
        self.assertEqual(1, hands[2, HQ])
        self.assertEqual(1, hands[1, C7])

    def test_calc_winner(self):
        trick = Trick(first_player=EAST)
        #                       E   N   W   S
        trick.cards = np.array([SA, SK, HQ, C7])
        self.assertEqual(trick.calc_winner(DIAMONDS), EAST)
        self.assertEqual(trick.calc_winner(HEARTS), WEST)
        self.assertEqual(trick.calc_winner(SPADES), EAST)
        self.assertEqual(trick.calc_winner(CLUBS), SOUTH)
        self.assertEqual(trick.calc_winner(OBE_ABE), EAST)
        self.assertEqual(trick.calc_winner(UNE_UFE), NORTH)

        #                       E   N    W   S
        trick.cards = np.array([S9, S10, SQ, SK])
        self.assertEqual(trick.calc_winner(SPADES), EAST)

        #                       E   N    W   S
        trick.cards = np.array([S9, S10, SJ, SK])
        self.assertEqual(trick.calc_winner(SPADES), WEST)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, SJ])
        self.assertEqual(trick.calc_winner(HEARTS), EAST)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, SJ])
        self.assertEqual(trick.calc_winner(DIAMONDS), WEST)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, SJ])
        self.assertEqual(trick.calc_winner(SPADES), SOUTH)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, S9])
        self.assertEqual(trick.calc_winner(SPADES), SOUTH)

        #                       E   N    W   S
        trick.cards = np.array([D7, SA, D6, S9])
        self.assertEqual(trick.calc_winner(UNE_UFE), WEST)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, S9])
        self.assertEqual(trick.calc_winner(UNE_UFE), SOUTH)

        #                       E   N    W   S
        trick.cards = np.array([SA, D6, D7, S9])
        self.assertEqual(trick.calc_winner(OBE_ABE), EAST)


if __name__ == '__main__':
    unittest.main()
