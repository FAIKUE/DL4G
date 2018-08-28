import unittest

from jass.base.const import *
from jass.base.round import Round
from jass.io.round_generator import RoundGenerator
from jass.io.round_parser import RoundParser


class RoundParserCase(unittest.TestCase):
    def test_generator_and_parser(self):
        # Generate a round manually by 'playing' a game
        rnd = Round(dealer=WEST)
        rnd.action_trump(PUSH)
        rnd.action_trump(U)
        rnd.action_play_card(C7)
        rnd.action_play_card(CK)
        rnd.action_play_card(C6)
        rnd.action_play_card(CJ)
        rnd.action_play_card(S7)
        rnd.action_play_card(SJ)
        rnd.action_play_card(SA)
        rnd.action_play_card(C10)
        rnd.action_play_card(S9)
        rnd.action_play_card(S6)
        rnd.action_play_card(SQ)
        rnd.action_play_card(D10)
        rnd.action_play_card(H10)
        rnd.action_play_card(HJ)
        rnd.action_play_card(H6)
        rnd.action_play_card(HQ)
        rnd.action_play_card(H7)
        rnd.action_play_card(DA)
        rnd.action_play_card(H8)
        rnd.action_play_card(C9)
        rnd.action_play_card(H9)
        rnd.action_play_card(CA)
        rnd.action_play_card(HA)
        rnd.action_play_card(DJ)
        rnd.action_play_card(HK)
        rnd.action_play_card(S8)
        rnd.action_play_card(SK)
        rnd.action_play_card(CQ)
        rnd.action_play_card(DQ)
        rnd.action_play_card(D6)
        rnd.action_play_card(D9)
        rnd.action_play_card(DK)
        rnd.action_play_card(S10)
        rnd.action_play_card(D7)
        rnd.action_play_card(C8)
        rnd.action_play_card(D8)
        rnd.assert_invariants()
        self.assertEqual(36, rnd.nr_played_cards)

        rnd_data = RoundGenerator.generate_dict(rnd)
        rnd_from_data = RoundParser.parse_round(rnd_data)

        # reconstructed round should be the same
        self.assertTrue(rnd == rnd_from_data)


if __name__ == '__main__':
    unittest.main()
