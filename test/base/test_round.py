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

    #def test_calc_winner_profiling(self):
        # for profiling: calll methods 1000 times
    #    for i in range(10000):
    #        self.test_calc_winner()

    def test_complete_round(self):
        # replay round manually from a log file entry
        # {"trump":5,"dealer":3,"tss":1,"tricks":[{"cards":["C7","CK","C6","CJ"],"points":17,"win":0,"first":2},
        rnd = Round(dealer=WEST)
        rnd.action_trump(PUSH)
        rnd.action_trump(U)

        rnd.action_play_card(C7)
        rnd.assert_invariants()

        rnd.action_play_card(CK)
        rnd.assert_invariants()

        rnd.action_play_card(C6)
        rnd.assert_invariants()

        rnd.action_play_card(CJ)
        rnd.assert_invariants()
        self.assertEqual(1, rnd.nr_tricks)
        self.assertEqual(17, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(2, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S7","SJ","SA","C10"],"points":12,"win":0,"first":0},
        rnd.action_play_card(S7), rnd.assert_invariants()
        rnd.action_play_card(SJ), rnd.assert_invariants()
        rnd.action_play_card(SA), rnd.assert_invariants()
        rnd.action_play_card(C10), rnd.assert_invariants()
        self.assertEqual(2, rnd.nr_tricks)
        self.assertEqual(12, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S9","S6","SQ","D10"],"points":24,"win":3,"first":0},
        rnd.action_play_card(S9), rnd.assert_invariants()
        rnd.action_play_card(S6), rnd.assert_invariants()
        rnd.action_play_card(SQ), rnd.assert_invariants()
        rnd.action_play_card(D10), rnd.assert_invariants()
        self.assertEqual(3, rnd.nr_tricks)
        self.assertEqual(24, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(3, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H10","HJ","H6","HQ"],"points":26,"win":1,"first":3},
        rnd.action_play_card(H10), rnd.assert_invariants()
        rnd.action_play_card(HJ), rnd.assert_invariants()
        rnd.action_play_card(H6), rnd.assert_invariants()
        rnd.action_play_card(HQ), rnd.assert_invariants()
        self.assertEqual(4, rnd.nr_tricks)
        self.assertEqual(26, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(3, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H7","DA","H8","C9"],"points":8,"win":1,"first":1},
        rnd.action_play_card(H7), rnd.assert_invariants()
        rnd.action_play_card(DA), rnd.assert_invariants()
        rnd.action_play_card(H8), rnd.assert_invariants()
        rnd.action_play_card(C9), rnd.assert_invariants()
        self.assertEqual(5, rnd.nr_tricks)
        self.assertEqual(8, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H9","CA","HA","DJ"],"points":2,"win":1,"first":1},
        rnd.action_play_card(H9), rnd.assert_invariants()
        rnd.action_play_card(CA), rnd.assert_invariants()
        rnd.action_play_card(HA), rnd.assert_invariants()
        rnd.action_play_card(DJ), rnd.assert_invariants()
        self.assertEqual(6, rnd.nr_tricks)
        self.assertEqual(2, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["HK","S8","SK","CQ"],"points":19,"win":1,"first":1},
        rnd.action_play_card(HK), rnd.assert_invariants()
        rnd.action_play_card(S8), rnd.assert_invariants()
        rnd.action_play_card(SK), rnd.assert_invariants()
        rnd.action_play_card(CQ), rnd.assert_invariants()
        self.assertEqual(7, rnd.nr_tricks)
        self.assertEqual(19, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["DQ","D6","D9","DK"],"points":18,"win":0,"first":1},
        rnd.action_play_card(DQ), rnd.assert_invariants()
        rnd.action_play_card(D6), rnd.assert_invariants()
        rnd.action_play_card(D9), rnd.assert_invariants()
        rnd.action_play_card(DK), rnd.assert_invariants()
        self.assertEqual(8, rnd.nr_tricks)
        self.assertEqual(18, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}]
        rnd.action_play_card(S10), rnd.assert_invariants()
        rnd.action_play_card(D7), rnd.assert_invariants()
        rnd.action_play_card(C8), rnd.assert_invariants()
        rnd.action_play_card(D8), rnd.assert_invariants()
        self.assertEqual(9, rnd.nr_tricks)
        self.assertEqual(31, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

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
