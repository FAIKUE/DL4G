import unittest

from jass.base.const import *
from jass.base.round import Round


class RoundTestCase(unittest.TestCase):

    def test_round_empty(self):
        rnd = Round()
        rnd.assert_invariants()

    def test_make_trump(self):
        rnd = Round(dealer=NORTH)
        rnd.action_trump(DIAMONDS)
        rnd.assert_invariants()

        rnd2 = Round(dealer=NORTH)
        rnd2.action_trump(PUSH)
        rnd.assert_invariants()
        rnd2.action_trump(DIAMONDS)
        rnd.assert_invariants()
        self.assertEqual(WEST, rnd2.player)

    def test_calc_points(self):
        trick = np.array([SA, SK, SQ, SJ])

        points = Round.calc_points(trick, trump=D, is_last=False)
        self.assertEqual(20, points)

        points = Round.calc_points(trick, trump=H, is_last=True)
        self.assertEqual(25, points)

        points = Round.calc_points(trick, trump=S, is_last=False)
        self.assertEqual(38, points)

        points = Round.calc_points(trick, trump=C, is_last=False)
        self.assertEqual(20, points)

        trick = np.array([SA, SJ, S6, S9])
        points = Round.calc_points(trick, trump=S, is_last=False)
        self.assertEqual(45, points)

    def test_calc_winner(self):
        first_player=EAST
        #                 E   N   W   S
        trick = np.array([SA, SK, HQ, C7])
        self.assertEqual(Round.calc_winner(trick, first_player, DIAMONDS), EAST)
        self.assertEqual(Round.calc_winner(trick, first_player, HEARTS), WEST)
        self.assertEqual(Round.calc_winner(trick, first_player, SPADES), EAST)
        self.assertEqual(Round.calc_winner(trick, first_player, CLUBS), SOUTH)
        self.assertEqual(Round.calc_winner(trick, first_player, OBE_ABE), EAST)
        self.assertEqual(Round.calc_winner(trick, first_player, UNE_UFE), NORTH)

        #                 E   N    W   S
        trick = np.array([S9, S10, SQ, SK])
        self.assertEqual(Round.calc_winner(trick, first_player, SPADES), EAST)

        #                 E   N    W   S
        trick = np.array([S9, S10, SJ, SK])
        self.assertEqual(Round.calc_winner(trick, first_player, SPADES), WEST)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        self.assertEqual(Round.calc_winner(trick, first_player,HEARTS), EAST)

        #                 E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        self.assertEqual(Round.calc_winner(trick, first_player,DIAMONDS), WEST)

        #                 E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        self.assertEqual(Round.calc_winner(trick, first_player,SPADES), SOUTH)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        self.assertEqual(Round.calc_winner(trick, first_player,SPADES), SOUTH)

        #                E   N    W   S
        trick = np.array([D7, SA, D6, S9])
        self.assertEqual(Round.calc_winner(trick, first_player,UNE_UFE), WEST)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        self.assertEqual(Round.calc_winner(trick, first_player,UNE_UFE), SOUTH)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        self.assertEqual(Round.calc_winner(trick, first_player,OBE_ABE), EAST)

    def test_calc_winner_profiling(self):
        # for profiling: calll methods 1000 times
        for i in range(10000):
            self.test_calc_winner()

    def test_deal(self):
        rnd = Round()
        rnd.deal_cards()
        # check if all 36 cards have been dealt
        self.assertEqual(36, rnd.hands.sum())

        # check if each player got 9 cards
        self.assertEqual(9, rnd.hands[0, :].sum())
        self.assertEqual(9, rnd.hands[1, :].sum())
        self.assertEqual(9, rnd.hands[2, :].sum())
        self.assertEqual(9, rnd.hands[3, :].sum())

        # check if each card has been dealt exactly once
        cards = rnd.hands.sum(axis=0)
        self.assertTrue(np.all(cards == np.ones(36, dtype=np.int32)))

        rnd.assert_invariants()

if __name__ == '__main__':
    unittest.main()
