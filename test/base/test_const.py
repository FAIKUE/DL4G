import unittest

from jass.base.const import *


class JassConstTestCase(unittest.TestCase):
    def test_card_values(self):
        for trump in range(MAX_TRUMP):
            # 152 points are possible without counting the bonus of the last trick
            self.assertEqual(152, card_values[trump, :].sum())

    def test_color_mask(self):
        for color in range(4):
            # 9 cards per color
            self.assertEqual(9, color_masks[color, :].sum())

    def test_same_player(self):
        self.assertTrue(same_team[0, 0])
        self.assertTrue(same_team[0, 2])
        self.assertTrue(same_team[2, 0])
        self.assertTrue(same_team[2, 2])
        self.assertTrue(same_team[1, 1])
        self.assertTrue(same_team[1, 3])
        self.assertTrue(same_team[3, 1])
        self.assertTrue(same_team[3, 3])

        self.assertFalse(same_team[0, 1])
        self.assertFalse(same_team[0, 3])
        self.assertFalse(same_team[1, 0])
        self.assertFalse(same_team[1, 2])
        self.assertFalse(same_team[2, 1])
        self.assertFalse(same_team[2, 3])
        self.assertFalse(same_team[3, 0])
        self.assertFalse(same_team[3, 2])


if __name__ == '__main__':
    unittest.main()
