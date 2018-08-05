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

if __name__ == '__main__':
    unittest.main()
