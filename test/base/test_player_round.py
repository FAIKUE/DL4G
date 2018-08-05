import unittest
from jass.base.const import *
from jass.base.round import Round
from jass.base.player_round import PlayerRound

class PlayerRoundTestCase(unittest.TestCase):
    def test_init(self):
        player_rnd = PlayerRound()

    def test_from_round(self):
        # create a full round
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

        for i in range(36):
            player_rnd = PlayerRound.from_complete_round(rnd, i)
            self.assertEqual(i, player_rnd.nr_played_cards)
            self.assertEqual(rnd.dealer, player_rnd.dealer)
            self.assertEqual(rnd.declared_trump, player_rnd.declared_trump)
            self.assertEqual(rnd.forehand, player_rnd.forehand)
            self.assertEqual(rnd.trump, player_rnd.trump)

            nr_tricks, nr_cards_in_trick = divmod(i, 4)
            self.assertEqual(nr_tricks, player_rnd.nr_tricks)
            self.assertEqual(nr_cards_in_trick, player_rnd.nr_cards_in_trick)


if __name__ == '__main__':
    unittest.main()
