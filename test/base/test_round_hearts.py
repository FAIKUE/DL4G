import unittest

from source.jass.base.const import *
from source.jass.base.round_hearts import RoundHeartsTeam


class RoundHeartsTestCase(unittest.TestCase):

    def test_round_empty(self):
        rnd = RoundHeartsTeam(dealer=NORTH)
        rnd.assert_invariants()

    def test_calc_points(self):
        rnd = RoundHeartsTeam(dealer=NORTH)
        trick = np.array([SA, SK, S6, SJ])

        points = rnd.rule.calc_points(trick, is_last=False)
        self.assertEqual(0, points)

        trick = np.array([HA, H6, HK, SJ])
        points = rnd.rule.calc_points(trick, is_last=True)
        self.assertEqual(-3, points)

        trick = np.array([SQ, H6, HK, SJ])
        points = rnd.rule.calc_points(trick, is_last=False)
        self.assertEqual(-11, points)

    def test_calc_winner(self):
        rnd = RoundHeartsTeam(dealer=NORTH)
        first_player = EAST
        #                 E   N   W   S
        trick = np.array([SA, SK, HQ, C7])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player), EAST)

        #                 E   N    W   S
        trick = np.array([S9, S10, SQ, SK])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player), SOUTH)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player), EAST)

        #                 E   N    W   S
        trick = np.array([SA, HA, DQ, C6])
        rnd.trump = SPADES
        self.assertEqual(rnd.rule.calc_winner(trick, first_player), EAST)

        #                E   N    W   S
        trick = np.array([D7, SA, D6, S9])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player), EAST)

    # def test_calc_winner_profiling(self):
        # for profiling: call methods 1000 times
    #    for i in range(10000):
    #        self.test_calc_winner()

    def test_complete_round(self):
        rnd = RoundHeartsTeam(dealer=WEST)
        rnd.action_play_card(C7)
        rnd.assert_invariants()

        rnd.action_play_card(CK)
        rnd.assert_invariants()

        rnd.action_play_card(C6)
        rnd.assert_invariants()

        rnd.action_play_card(CJ)
        rnd.assert_invariants()
        self.assertEqual(1, rnd.nr_tricks)
        self.assertEqual(0, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(S7), rnd.assert_invariants()
        rnd.action_play_card(SJ), rnd.assert_invariants()
        rnd.action_play_card(SA), rnd.assert_invariants()
        rnd.action_play_card(C10), rnd.assert_invariants()
        self.assertEqual(2, rnd.nr_tricks)
        self.assertEqual(0, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(S9), rnd.assert_invariants()
        rnd.action_play_card(S6), rnd.assert_invariants()
        rnd.action_play_card(SQ), rnd.assert_invariants()
        rnd.action_play_card(D10), rnd.assert_invariants()
        self.assertEqual(3, rnd.nr_tricks)
        self.assertEqual(-9, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(H10), rnd.assert_invariants()
        rnd.action_play_card(HJ), rnd.assert_invariants()
        rnd.action_play_card(H6), rnd.assert_invariants()
        rnd.action_play_card(HQ), rnd.assert_invariants()
        self.assertEqual(4, rnd.nr_tricks)
        self.assertEqual(-4, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(H7), rnd.assert_invariants()
        rnd.action_play_card(DA), rnd.assert_invariants()
        rnd.action_play_card(H8), rnd.assert_invariants()
        rnd.action_play_card(C9), rnd.assert_invariants()
        self.assertEqual(5, rnd.nr_tricks)
        self.assertEqual(-2, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(NORTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(H9), rnd.assert_invariants()
        rnd.action_play_card(CA), rnd.assert_invariants()
        rnd.action_play_card(HA), rnd.assert_invariants()
        rnd.action_play_card(DJ), rnd.assert_invariants()
        self.assertEqual(6, rnd.nr_tricks)
        self.assertEqual(-2, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(NORTH, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(HK), rnd.assert_invariants()
        rnd.action_play_card(S8), rnd.assert_invariants()
        rnd.action_play_card(SK), rnd.assert_invariants()
        rnd.action_play_card(CQ), rnd.assert_invariants()
        self.assertEqual(7, rnd.nr_tricks)
        self.assertEqual(-1, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_first_player[rnd.nr_tricks-1])

        rnd.action_play_card(DQ), rnd.assert_invariants()
        rnd.action_play_card(D6), rnd.assert_invariants()
        rnd.action_play_card(D9), rnd.assert_invariants()
        rnd.action_play_card(DK), rnd.assert_invariants()
        self.assertEqual(8, rnd.nr_tricks)
        self.assertEqual(0, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(SOUTH, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}]
        rnd.action_play_card(S10), rnd.assert_invariants()
        rnd.action_play_card(D7), rnd.assert_invariants()
        rnd.action_play_card(C8), rnd.assert_invariants()
        rnd.action_play_card(D8), rnd.assert_invariants()
        self.assertEqual(9, rnd.nr_tricks)
        self.assertEqual(0, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_first_player[rnd.nr_tricks-1])

        # test equality operator
        self.assertTrue(rnd == rnd)

    def test_deal(self):
        rnd = RoundHeartsTeam(dealer=NORTH)
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
