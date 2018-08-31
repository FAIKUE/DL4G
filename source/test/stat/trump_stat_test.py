import unittest

from jass.stat.trump_stat import *


class TrumpStatTestCase(unittest.TestCase):

    def test_trump5(self):
        r = Round()
        r.trump = 0
        r.forehand = True
        r.declared_trump = 0
        hands = np.zeros([4, 36], np.int32)

        # fill played_cards for player 0

        # five trumps
        hands[0, DA] = 1
        hands[0, DK] = 1
        hands[0, DJ] = 1
        hands[0, D9] = 1
        hands[0, D8] = 1
        hands[0, CA] = 1
        hands[0, H6] = 1
        hands[0, H10] = 1
        hands[0, SQ] = 1
        r.played_cards = hands

        all_stat = AllStat()

        stat_true = JackNine5orMoreStat()
        stat_false_1 = JackNine4()
        stat_false_2 = JackNine3()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_round(r)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        r.trump = 1
        all_stat.add_round(r)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump4(self):
        r = Round()
        r.trump = 0
        r.forehand = True
        r.declared_trump = 0
        hands = np.zeros([4, 36], np.int32)

        # fill played_cards for player 0

        # four trumps
        hands[0, DA] = 1
        hands[0, DK] = 1
        hands[0, DJ] = 1
        hands[0, D9] = 1
        hands[0, H8] = 1
        hands[0, CA] = 1
        hands[0, H6] = 1
        hands[0, H10] = 1
        hands[0, SQ] = 1
        r.played_cards = hands

        all_stat = AllStat()

        stat_true = JackNine4()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine3()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_round(r)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        r.trump = 1
        all_stat.add_round(r)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump3(self):
        r = Round()
        r.trump = 0
        r.forehand = True
        r.declared_trump = 0
        hands = np.zeros([4, 36], np.int32)

        # fill played_cards for player 0

        # three trumps
        hands[0, DA] = 1
        hands[0, HK] = 1
        hands[0, DJ] = 1
        hands[0, D9] = 1
        hands[0, H8] = 1
        hands[0, CA] = 1
        hands[0, H6] = 1
        hands[0, H10] = 1
        hands[0, SQ] = 1
        r.played_cards = hands

        all_stat = AllStat()

        stat_true = JackNine3()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine4()
        stat_false_3 = Aces4()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_round(r)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        r.trump = 1
        all_stat.add_round(r)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

    def test_trump_4aces(self):
        r = Round()
        r.trump = OBE_ABE
        r.forehand = True
        r.declared_trump = 0
        hands = np.zeros([4, 36], np.int32)

        # fill played_cards for player 0

        # 4 aces
        hands[0, DA] = 1
        hands[0, HA] = 1
        hands[0, DJ] = 1
        hands[0, D8] = 1
        hands[0, H8] = 1
        hands[0, CA] = 1
        hands[0, H6] = 1
        hands[0, H10] = 1
        hands[0, SA] = 1
        r.played_cards = hands

        all_stat = AllStat()

        stat_true = Aces4()
        stat_false_1 = JackNine5orMoreStat()
        stat_false_2 = JackNine4()
        stat_false_3 = JackNine3()

        all_stat.add_statistic(stat_true)
        all_stat.add_statistic(stat_false_1)
        all_stat.add_statistic(stat_false_2)
        all_stat.add_statistic(stat_false_3)

        all_stat.add_round(r)

        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(0, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)

        for stat in [stat_false_1, stat_false_2, stat_false_3]:
            self.assertEqual(0, stat.counter_pos_forehand)
            self.assertEqual(0, stat.counter_neg_forehand)
            self.assertEqual(0, stat.counter_pos_rearhand)
            self.assertEqual(0, stat.counter_neg_rearhand)

        r.trump = 1
        all_stat.add_round(r)
        self.assertEqual(1, stat_true.counter_pos_forehand)
        self.assertEqual(1, stat_true.counter_neg_forehand)
        self.assertEqual(0, stat_true.counter_pos_rearhand)
        self.assertEqual(0, stat_true.counter_neg_rearhand)


if __name__ == '__main__':
    unittest.main()
