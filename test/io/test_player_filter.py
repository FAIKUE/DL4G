import unittest

from jass.io.player_filter import PlayerStatFilter, FilterMeanAbsolute, FilterStdAbsolute, FilterMeanRelative, \
    FilterStdRelative, FilterPlayedGamesRelative, FilterPlayedGamesAbsolute


class TestPlayerFilter(unittest.TestCase):

    def setUp(self):
        self.testee = PlayerStatFilter("..//resources//small_player_stat.json")

    def test_initialize_reads_all_data(self):
        self.assertEqual(20, len(self.testee._player_stats))

    def test_filter_mean_abs(self):
        fltr = FilterMeanAbsolute(80)
        self.testee.add_filter(fltr)

        player_stat = self.testee.filter()
        self.assertEqual(5, len(player_stat))

    def test_filter_std_abs(self):
        fltr = FilterStdAbsolute(42)
        self.testee.add_filter(fltr)
        player_stat = self.testee.filter()

        self.assertEqual(5, len(player_stat))

    def test_filter_mean_rel(self):
        fltr = FilterMeanRelative(0.25)
        self.testee.add_filter(fltr)
        player_stat = self.testee.filter()

        self.assertEqual(15, len(player_stat))

    def test_filter_std_rel(self):
        fltr = FilterStdRelative(0.25)
        self.testee.add_filter(fltr)
        player_stat = self.testee.filter()

        self.assertEqual(15, len(player_stat))

    def test_filter_played_games_absolute(self):
        fltr = FilterPlayedGamesAbsolute(2000)
        self.testee.add_filter(fltr)
        player_stat = self.testee.filter()

        self.assertEqual(11, len(player_stat))

    def test_filter_played_games_rel(self):
        fltr = FilterPlayedGamesRelative(0.25)
        self.testee.add_filter(fltr)
        player_stat = self.testee.filter()

        self.assertEqual(15, len(player_stat))

    def test_multiple_absolute_filters(self):
        fltr_one = FilterMeanAbsolute(80)
        fltr_two = FilterStdAbsolute(42.5)
        self.testee.add_filter(fltr_one)
        self.testee.add_filter(fltr_two)

        player_stat = self.testee.filter()

        self.assertEqual(4, len(player_stat))

    def test_multiple_filters(self):
        fltr_one = FilterMeanRelative(0.5)
        fltr_two = FilterStdRelative(0.5)
        self.testee.add_filter(fltr_one)
        self.testee.add_filter(fltr_two)

        player_stat = self.testee.filter()

        self.assertEqual(3, len(player_stat))

    def test_filter_rel_mean_0_raises_exception(self):
        with self.assertRaises(Exception):
            fltr = FilterMeanRelative(0)
            self.testee.add_filter(fltr)
            self.testee.filter()

    def test_filter_rel_mean_1_raises_exception(self):
        with self.assertRaises(Exception):
            fltr = FilterMeanRelative(1)
            self.testee.add_filter(fltr)
            self.testee.filter()

    def test_filter_rel_std_0_raises_exception(self):
        with self.assertRaises(Exception):
            fltr = FilterStdRelative(0)
            self.testee.add_filter(fltr)
            self.testee.filter()

    def test_filter_rel_std_1_raises_exception(self):
        with self.assertRaises(Exception):
            fltr = FilterStdRelative(1)
            self.testee.add_filter(fltr)
            self.testee.filter()

