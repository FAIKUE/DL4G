import unittest

from jass.base.const import *
from jass.base.round_schieber import RoundSchieber


class RoundTestCase(unittest.TestCase):

    def test_round_empty(self):
        rnd = RoundSchieber(dealer=NORTH)
        rnd.deal_cards()
        rnd.assert_invariants()

    def test_make_trump(self):
        rnd = RoundSchieber(dealer=NORTH)
        rnd.deal_cards()
        rnd.action_trump(DIAMONDS)
        rnd.assert_invariants()

        rnd2 = RoundSchieber(dealer=NORTH)
        rnd2.deal_cards()
        rnd2.action_trump(PUSH)
        rnd2.assert_invariants()
        rnd2.action_trump(DIAMONDS)
        rnd2.assert_invariants()
        self.assertEqual(WEST, rnd2.player)

    def test_calc_points(self):
        rnd = RoundSchieber(dealer=NORTH)
        trick = np.array([SA, SK, SQ, SJ])
        rnd.trump = DIAMONDS
        points = rnd.rule.calc_points(trick, is_last=False, trump=DIAMONDS)
        self.assertEqual(20, points)

        rnd.trump = HEARTS
        points = rnd.rule.calc_points(trick, is_last=True, trump=HEARTS)
        self.assertEqual(25, points)

        rnd.trump = SPADES
        points = rnd.rule.calc_points(trick, is_last=False, trump=SPADES)
        self.assertEqual(38, points)

        rnd.trump = CLUBS
        points = rnd.rule.calc_points(trick, is_last=False, trump=CLUBS)
        self.assertEqual(20, points)

        trick = np.array([SA, SJ, S6, S9])
        rnd.trump = SPADES
        points = rnd.rule.calc_points(trick, is_last=False, trump=SPADES)
        self.assertEqual(45, points)

    def test_calc_winner(self):
        rnd = RoundSchieber(dealer=NORTH)
        first_player = EAST
        #                 E   N   W   S
        trick = np.array([SA, SK, HQ, C7])
        rnd.trump = DIAMONDS
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=DIAMONDS), EAST)
        rnd.trump = HEARTS
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=HEARTS), WEST)
        rnd.trump = SPADES
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=SPADES), EAST)
        rnd.trump = CLUBS
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=CLUBS), SOUTH)
        rnd.trump = OBE_ABE
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=OBE_ABE), EAST)
        rnd.trump = UNE_UFE
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=UNE_UFE), NORTH)

        #                 E   N    W   S
        trick = np.array([S9, S10, SQ, SK])
        rnd.trump = SPADES
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=SPADES), EAST)

        #                 E   N    W   S
        trick = np.array([S9, S10, SJ, SK])
        rnd.trump = SPADES
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=SPADES), WEST)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        rnd.trump = HEARTS
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=HEARTS), EAST)

        #                 E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        rnd.trump = DIAMONDS
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=DIAMONDS), WEST)

        #                 E   N    W   S
        trick = np.array([SA, D6, D7, SJ])
        rnd.trump = SPADES
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=SPADES), SOUTH)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=SPADES), SOUTH)

        #                E   N    W   S
        trick = np.array([D7, SA, D6, S9])
        rnd.trump = UNE_UFE
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=UNE_UFE), WEST)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=UNE_UFE), SOUTH)

        #                E   N    W   S
        trick = np.array([SA, D6, D7, S9])
        rnd.trump = OBE_ABE
        self.assertEqual(rnd.rule.calc_winner(trick, first_player, trump=OBE_ABE), EAST)

    # def test_calc_winner_profiling(self):
        # for profiling: call methods 1000 times
    #    for i in range(10000):
    #        self.test_calc_winner()

    def test_complete_round(self):
        # replay round manually from a log file entry
        # {"trump":5,"dealer":3,"tss":1,"tricks":[{"cards":["C7","CK","C6","CJ"],"points":17,"win":0,"first":2},
        rnd = RoundSchieber(dealer=WEST)
        hands = np.array([
            get_cards_encoded([C6, S7, S9, HQ, DA, CA, S8, D6, S10]),      # N
            get_cards_encoded([CK, C10, D10, H6, H7, H9, HK, DQ, D8]),     # E
            get_cards_encoded([C7, SA, SQ, HJ, C9, DJ, CQ, DK, C8]),       # S
            get_cards_encoded([CJ, SJ, S6, H10, H8, HA, SK, D9, D7 ]),     # W
        ], dtype=np.int32)
        rnd.set_hands(hands)
        rnd.action_trump(PUSH)
        rnd.action_trump(U)

        rnd.action_play_card(C7)        # S
        rnd.assert_invariants()

        rnd.action_play_card(CK)        # E
        rnd.assert_invariants()

        rnd.action_play_card(C6)        # N
        rnd.assert_invariants()

        rnd.action_play_card(CJ)        # W
        rnd.assert_invariants()
        self.assertEqual(1, rnd.nr_tricks)
        self.assertEqual(17, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(NORTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(2, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S7","SJ","SA","C10"],"points":12,"win":0,"first":0},
        rnd.action_play_card(S7), rnd.assert_invariants() # N
        rnd.action_play_card(SJ), rnd.assert_invariants() # W
        rnd.action_play_card(SA), rnd.assert_invariants() # S
        rnd.action_play_card(C10), rnd.assert_invariants() # E
        self.assertEqual(2, rnd.nr_tricks)
        self.assertEqual(12, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(NORTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S9","S6","SQ","D10"],"points":24,"win":3,"first":0},
        rnd.action_play_card(S9), rnd.assert_invariants() # N
        rnd.action_play_card(S6), rnd.assert_invariants()
        rnd.action_play_card(SQ), rnd.assert_invariants()
        rnd.action_play_card(D10), rnd.assert_invariants()
        self.assertEqual(3, rnd.nr_tricks)
        self.assertEqual(24, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(WEST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H10","HJ","H6","HQ"],"points":26,"win":1,"first":3},
        rnd.action_play_card(H10), rnd.assert_invariants() #W
        rnd.action_play_card(HJ), rnd.assert_invariants()
        rnd.action_play_card(H6), rnd.assert_invariants()
        rnd.action_play_card(HQ), rnd.assert_invariants()
        self.assertEqual(4, rnd.nr_tricks)
        self.assertEqual(26, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(3, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H7","DA","H8","C9"],"points":8,"win":1,"first":1},
        rnd.action_play_card(H7), rnd.assert_invariants() # E
        rnd.action_play_card(DA), rnd.assert_invariants()
        rnd.action_play_card(H8), rnd.assert_invariants()
        rnd.action_play_card(C9), rnd.assert_invariants()
        self.assertEqual(5, rnd.nr_tricks)
        self.assertEqual(8, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["H9","CA","HA","DJ"],"points":2,"win":1,"first":1},
        rnd.action_play_card(H9), rnd.assert_invariants() # E
        rnd.action_play_card(CA), rnd.assert_invariants()
        rnd.action_play_card(HA), rnd.assert_invariants()
        rnd.action_play_card(DJ), rnd.assert_invariants()
        self.assertEqual(6, rnd.nr_tricks)
        self.assertEqual(2, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["HK","S8","SK","CQ"],"points":19,"win":1,"first":1},
        rnd.action_play_card(HK), rnd.assert_invariants() # E
        rnd.action_play_card(S8), rnd.assert_invariants()
        rnd.action_play_card(SK), rnd.assert_invariants()
        rnd.action_play_card(CQ), rnd.assert_invariants()
        self.assertEqual(7, rnd.nr_tricks)
        self.assertEqual(19, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(EAST, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["DQ","D6","D9","DK"],"points":18,"win":0,"first":1},
        rnd.action_play_card(DQ), rnd.assert_invariants() # E
        rnd.action_play_card(D6), rnd.assert_invariants()
        rnd.action_play_card(D9), rnd.assert_invariants()
        rnd.action_play_card(DK), rnd.assert_invariants()
        self.assertEqual(8, rnd.nr_tricks)
        self.assertEqual(18, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(NORTH, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(1, rnd.trick_first_player[rnd.nr_tricks-1])

        # {"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}]
        rnd.action_play_card(S10), rnd.assert_invariants() #N
        rnd.action_play_card(D7), rnd.assert_invariants()
        rnd.action_play_card(C8), rnd.assert_invariants()
        rnd.action_play_card(D8), rnd.assert_invariants()
        self.assertEqual(9, rnd.nr_tricks)
        self.assertEqual(31, rnd.trick_points[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_winner[rnd.nr_tricks-1])
        self.assertEqual(0, rnd.trick_first_player[rnd.nr_tricks-1])

        # test equality operator
        self.assertTrue(rnd == rnd)

    def test_deal(self):
        rnd = RoundSchieber()
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
