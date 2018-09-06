import unittest

from jass.stat.trump_stat import *


class TrumpStatTestCase(unittest.TestCase):

    def test_trump5(self):
        trump = 0
        forehand = True
        hands = np.zeros([36], np.int32)

        # fill played_cards for player 0

        # five trumps
        hands[DA] = 1
        hands[DK] = 1
        hands[DJ] = 1
        hands[D9] = 1
        hands[D8] = 1
        hands[CA] = 1
        hands[H6] = 1
        hands[H10] = 1
        hands[SQ] = 1

        all_stat = AllStat()

        stat_true = JackNine5orMoreStat()
        stat_false_1 = JackNine4()
        stat_false_2 = JackNine3()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_hand(hands, trump, forehand)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        trump = 1
        all_stat.add_hand(hands, trump, forehand)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump4(self):
        trump = 0
        forehand = True
        hands = np.zeros([36], np.int32)

        # fill played_cards for player 0

        # four trumps
        hands[DA] = 1
        hands[DK] = 1
        hands[DJ] = 1
        hands[D9] = 1
        hands[H8] = 1
        hands[CA] = 1
        hands[H6] = 1
        hands[H10] = 1
        hands[SQ] = 1

        all_stat = AllStat()

        stat_true = JackNine4()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine3()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_hand(hands, trump, forehand)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        trump = 1
        all_stat.add_hand(hands, trump, forehand)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump3(self):
        trump = 0
        forehand = True
        hands = np.zeros([36], np.int32)

        # fill played_cards for player 0

        # three trumps
        hands[DA] = 1
        hands[HK] = 1
        hands[DJ] = 1
        hands[D9] = 1
        hands[H8] = 1
        hands[CA] = 1
        hands[H6] = 1
        hands[H10] = 1
        hands[SQ] = 1

        all_stat = AllStat()

        stat_true = JackNine3()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine4()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_hand(hands, trump, forehand)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        trump = 1
        all_stat.add_hand(hands, trump, forehand)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump_4aces(self):
        trump = OBE_ABE
        forehand = True
        hands = np.zeros([36], np.int32)

        # fill played_cards for player 0

        # 4 aces
        hands[DA] = 1
        hands[HA] = 1
        hands[DJ] = 1
        hands[D8] = 1
        hands[H8] = 1
        hands[CA] = 1
        hands[H6] = 1
        hands[H10] = 1
        hands[SA] = 1

        all_stat = AllStat()

        stat_true = Aces4()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine4()
        stat_false_3 = JackNine3()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_hand(hands, trump, forehand)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        trump = 1
        all_stat.add_hand(hands, trump, forehand)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)


if __name__ == '__main__':
    unittest.main()
