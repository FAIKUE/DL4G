import unittest
from source.jass.base.const import *
from source.jass.base.rule_hearts import RuleHearts


class RuleHeartsTestCase(unittest.TestCase):
    def setUp(self):
        self.hand = np.zeros(36, np.int32)
        self.rule = RuleHearts()

    def test_valid_cards(self):
        self.hand[[SA, SK, H7, HJ]] = 1

        # no color in hand
        valid = self.rule.get_valid_cards(self.hand, [CA], 1, None)
        self.assertTrue(np.all(self.hand == valid))

        valid = self.rule.get_valid_cards(self.hand, [C6], 1, None)
        self.assertTrue(np.all(self.hand == valid))

        # color in hand
        valid = self.rule.get_valid_cards(self.hand, [SQ], 1, None)
        expected = np.zeros(36, np.int32)
        expected[[SA, SK]] = 1
        self.assertTrue(np.all(expected == valid))

        valid = self.rule.get_valid_cards(self.hand, [S7], 1, None)
        self.assertTrue(np.all(expected == valid))

    def test_first_move(self):
        self.hand[[SA, SK, H7, HJ, C6, C7, D10]] = 1
        valid = self.rule.get_valid_cards(self.hand, [], 0, None)
        self.assertTrue(np.all(self.hand == valid))

    def test_other_color(self):
        self.hand[[SA, SK, HJ, C6, C7]] = 1
        valid = self.rule.get_valid_cards(self.hand, [S10, C6], 2, None)

        # give color
        expected = np.zeros(36, np.int32)
        expected[[SA, SK]] = 1
        self.assertTrue(np.all(expected == valid))

        # do not have the color, so any card is fine
        valid = self.rule.get_valid_cards(self.hand, [DA, DK, D10], 3, None)
        self.assertTrue(np.all(self.hand == valid))


if __name__ == '__main__':
    unittest.main()
