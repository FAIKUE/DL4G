import unittest

from jass.base.const import *
from jass.base.player_round import PlayerRound
from jass.base.round_factory import get_round, get_round_from_player_round
from jass.base.round_hearts import RoundHeartsTeam
from jass.base.round_schieber import RoundSchieber
from jass.base.rule_hearts import RuleHearts
from jass.base.rule_schieber import RuleSchieber


class RoundFactoryTestCase(unittest.TestCase):
    def test_factory(self):
        rnd = get_round(JASS_HEARTS)
        self.assertEqual(rnd.jass_type, JASS_HEARTS)
        self.assertIsInstance(rnd, RoundHeartsTeam)
        self.assertIsInstance(rnd.rule, RuleHearts)

        rnd = get_round(JASS_SCHIEBER_1000)
        self.assertEqual(rnd.jass_type, JASS_SCHIEBER_1000)
        self.assertIsInstance(rnd, RoundSchieber)
        self.assertIsInstance(rnd.rule, RuleSchieber)

        rnd = get_round(JASS_SCHIEBER_2500)
        self.assertEqual(rnd.jass_type, JASS_SCHIEBER_2500)
        self.assertIsInstance(rnd, RoundSchieber)
        self.assertIsInstance(rnd.rule, RuleSchieber)

    def test_round_from_player_round(self):
        hands = np.array([
            get_cards_encoded([DK, H10, S8, C8, C9, H8, D8, H9, H6]),
            get_cards_encoded([D10, HK, SK, CA, C10, SA, D9, C6, S10]),
            get_cards_encoded([D7, HJ, S7, C7, CK, S6, DJ, SQ, S9]),
            get_cards_encoded([D6, HQ, SJ, CQ, CJ, HA, DQ, DA, H7]),
        ], dtype=np.int32)

        player_rnd = PlayerRound(dealer = NORTH, jass_type=JASS_SCHIEBER_1000)
        player_rnd.hand = hands[WEST,:]

        # should be correct state for before trump
        player_rnd.assert_invariants()

        rnd = get_round_from_player_round(player_rnd, hands)
        rnd.assert_invariants()

        # Jass round does not support playing card actions, so we have to
        # adapt the state manually


        # Player west played a card, so now it is south turn

        hands[WEST, HA] = 0
        player_rnd = PlayerRound(dealer=NORTH, jass_type=JASS_SCHIEBER_1000)
        player_rnd.tricks[0, 0] = HA
        player_rnd.trump = OBE_ABE
        player_rnd.declared_trump = WEST
        player_rnd.forehand = True
        player_rnd.hand = hands[SOUTH, :]
        player_rnd.player = SOUTH
        player_rnd.nr_played_cards = 1
        player_rnd.nr_cards_in_trick = 1
        player_rnd.trick_first_player[0] = next_player[player_rnd.dealer]
        player_rnd.assert_invariants()

        rnd = get_round_from_player_round(player_rnd, hands)
        rnd.assert_invariants()


if __name__ == '__main__':
    unittest.main()
