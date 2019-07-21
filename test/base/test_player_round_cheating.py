import unittest
import json

from jass.base.const import *
from jass.base.round_schieber import RoundSchieber
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.io.log_parser_swisslos import LogParserSwisslos
from jass.io.round_serializer import RoundSerializer


class PlayerRoundCheatingTestCase(unittest.TestCase):
    def test_init(self):
        _ = PlayerRoundCheating()

    def test_from_round(self):
        # create a full round
        rnd = RoundSchieber(dealer=WEST)
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
            player_rnd = PlayerRoundCheating.from_complete_round(rnd, i)
            player_rnd.assert_invariants()
            self.assertEqual(i, player_rnd.nr_played_cards)

            self.assertEqual(rnd.declared_trump, player_rnd.declared_trump)
            self.assertEqual(rnd.forehand, player_rnd.forehand)
            self.assertEqual(rnd.trump, player_rnd.trump)

            nr_tricks, nr_cards_in_trick = divmod(i, 4)
            self.assertEqual(nr_tricks, player_rnd.nr_tricks)
            self.assertEqual(nr_cards_in_trick, player_rnd.nr_cards_in_trick)

        player_rnd = PlayerRoundCheating.trump_from_complete_round(rnd, forehand=True)
        self.assertEqual(rnd.dealer, player_rnd.dealer)
        self.assertIsNone(player_rnd.trump)
        self.assertIsNone(player_rnd.forehand)
        self.assertEqual(player_rnd.player, next_player[WEST])
        player_rnd.assert_invariants()

        player_rnd = PlayerRoundCheating.trump_from_complete_round(rnd, forehand=False)
        self.assertEqual(rnd.dealer, player_rnd.dealer)
        self.assertIsNone(player_rnd.trump)
        self.assertFalse(player_rnd.forehand)
        self.assertEqual(player_rnd.player, partner_player[next_player[WEST]])
        player_rnd.assert_invariants()

    def test_game_state_from_round(self):
        # take game string from a record
        round_string = '{"trump":5,"dealer":3,"tss":1,"tricks":[' \
                       '{"cards":["C7","CK","C6","CJ"],"points":17,"win":0,"first":2},' \
                       '{"cards":["S7","SJ","SA","C10"],"points":12,"win":0,"first":0},' \
                       '{"cards":["S9","S6","SQ","D10"],"points":24,"win":3,"first":0},' \
                       '{"cards":["H10","HJ","H6","HQ"],"points":26,"win":1,"first":3},' \
                       '{"cards":["H7","DA","H8","C9"],"points":8,"win":1,"first":1},' \
                       '{"cards":["H9","CA","HA","DJ"],"points":2,"win":1,"first":1},' \
                       '{"cards":["HK","S8","SK","CQ"],"points":19,"win":1,"first":1},' \
                       '{"cards":["DQ","D6","D9","DK"],"points":18,"win":0,"first":1},' \
                       '{"cards":["S10","D7","C8","D8"],"points":31,"win":0,"first":0}],' \
                       '"player":[{"hand":[]},{"hand":[]},{"hand":[]},{"hand":[]}],"jassTyp":"SCHIEBER_2500"}'
        round_dict = json.loads(round_string)
        rnd = RoundSerializer.round_from_dict(round_dict)
        player_rnds = PlayerRoundCheating.all_from_complete_round(rnd)
        self.assertEqual(36, len(player_rnds))

        # check properties for all moves
        for player_rnd in player_rnds:
            self.assertEqual(5, player_rnd.trump)
            self.assertEqual(3, player_rnd.dealer)
            self.assertEqual(0, player_rnd.declared_trump)
            self.assertEqual(False, player_rnd.forehand)
            player_rnd.assert_invariants()

        # first trick
        player_rnd = player_rnds[0]
        self.assertEqual(2, player_rnd.player)
        self.assertEqual(36, np.sum(player_rnd.hands))
        self.assertEqual(9, np.sum(player_rnd.hands[0, :]))
        self.assertEqual(9, np.sum(player_rnd.hands[1, :]))
        self.assertEqual(9, np.sum(player_rnd.hands[2, :]))
        self.assertEqual(9, np.sum(player_rnd.hands[3, :]))
        self.assertEqual(0, player_rnd.nr_played_cards)
        self.assertEqual(0, player_rnd.nr_tricks)
        self.assertEqual(0, player_rnd.nr_cards_in_trick)
        self.assertTrue(np.all(player_rnd.hands[player_rnd.player, :] == get_cards_encoded([C7, SA, SQ, HJ, C9, DJ, CQ, DK, C8])))
        self.assertEqual(0, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[1]
        self.assertEqual(1, player_rnd.player)
        self.assertEqual(35, np.sum(player_rnd.hands))
        self.assertEqual(1, player_rnd.nr_played_cards)
        self.assertEqual(0, player_rnd.nr_tricks)
        self.assertEqual(1, player_rnd.nr_cards_in_trick)
        self.assertEqual(C7, player_rnd.current_trick[0])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(0, player_rnd.points_team_0)

        player_rnd = player_rnds[2]
        self.assertEqual(0, player_rnd.player, 0)
        self.assertEqual(34, np.sum(player_rnd.hands))
        self.assertEqual(2, player_rnd.nr_played_cards)
        self.assertEqual(0, player_rnd.nr_tricks)
        self.assertEqual(2, player_rnd.nr_cards_in_trick)
        self.assertEqual(C7, player_rnd.current_trick[0])
        self.assertEqual(CK, player_rnd.current_trick[1])
        self.assertEqual(0, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[3]
        self.assertEqual(3, player_rnd.player)
        self.assertEqual(33, np.sum(player_rnd.hands))
        self.assertEqual(3, player_rnd.nr_played_cards)
        self.assertEqual(0, player_rnd.nr_tricks)
        self.assertEqual(3, player_rnd.nr_cards_in_trick)
        self.assertTrue([C6, C7, CK], player_rnd.nr_cards_in_trick)
        self.assertEqual(C7, player_rnd.current_trick[0])
        self.assertEqual(CK, player_rnd.current_trick[1])
        self.assertEqual(C6, player_rnd.current_trick[2])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(0, player_rnd.points_team_0)

        # second trick
        player_rnd = player_rnds[4]
        self.assertEqual(0, player_rnd.player)
        self.assertEqual(32, np.sum(player_rnd.hands))
        self.assertEqual(4, player_rnd.nr_played_cards)
        self.assertEqual(1, player_rnd.nr_tricks)
        self.assertEqual(0, player_rnd.nr_cards_in_trick)
        self.assertEqual(C7, player_rnd.tricks[0, 0])
        self.assertEqual(CK, player_rnd.tricks[0, 1])
        self.assertEqual(C6, player_rnd.tricks[0, 2])
        self.assertEqual(CJ, player_rnd.tricks[0, 3])
        self.assertEqual(17, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[5]
        self.assertEqual(3, player_rnd.player)
        self.assertEqual(31, np.sum(player_rnd.hands))
        self.assertEqual(5, player_rnd.nr_played_cards)
        self.assertEqual(1, player_rnd.nr_tricks, 1)
        self.assertEqual(1, player_rnd.nr_cards_in_trick)
        self.assertEqual(S7, player_rnd.current_trick[0])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(17, player_rnd.points_team_0)

        player_rnd = player_rnds[6]
        self.assertEqual(2, player_rnd.player, 2)
        self.assertEqual(30, np.sum(player_rnd.hands))
        self.assertEqual(6, player_rnd.nr_played_cards)
        self.assertEqual(1, player_rnd.nr_tricks, 1)
        self.assertEqual(2, player_rnd.nr_cards_in_trick)
        self.assertEqual(S7, player_rnd.current_trick[0])
        self.assertEqual(SJ, player_rnd.current_trick[1])
        self.assertEqual(17, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[7]
        self.assertEqual(1, player_rnd.player, 1)
        self.assertEqual(29, np.sum(player_rnd.hands))
        self.assertEqual(7, player_rnd.nr_played_cards)
        self.assertEqual(1, player_rnd.nr_tricks)
        self.assertEqual(3, player_rnd.nr_cards_in_trick)
        self.assertEqual(S7, player_rnd.current_trick[0])
        self.assertEqual(SJ, player_rnd.current_trick[1])
        self.assertEqual(SA, player_rnd.current_trick[2])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(17, player_rnd.points_team_0)

        # third trick
        player_rnd = player_rnds[8]
        self.assertEqual(0, player_rnd.player)
        self.assertEqual(28, np.sum(player_rnd.hands))
        self.assertEqual(8, player_rnd.nr_played_cards)
        self.assertEqual(2, player_rnd.nr_tricks)
        self.assertEqual(0, player_rnd.nr_cards_in_trick)
        self.assertEqual(C7, player_rnd.tricks[0, 0])
        self.assertEqual(CK, player_rnd.tricks[0, 1])
        self.assertEqual(C6, player_rnd.tricks[0, 2])
        self.assertEqual(CJ, player_rnd.tricks[0, 3])
        self.assertEqual(S7, player_rnd.tricks[1, 0])
        self.assertEqual(SJ, player_rnd.tricks[1, 1])
        self.assertEqual(SA, player_rnd.tricks[1, 2])
        self.assertEqual(C10, player_rnd.tricks[1, 3])
        self.assertEqual(29, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[9]
        self.assertEqual(3, player_rnd.player)
        self.assertEqual(27, np.sum(player_rnd.hands))
        self.assertEqual(9, player_rnd.nr_played_cards)
        self.assertEqual(2, player_rnd.nr_tricks)
        self.assertEqual(1, player_rnd.nr_cards_in_trick)
        self.assertEqual(S9, player_rnd.current_trick[0])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(29, player_rnd.points_team_0)

        player_rnd = player_rnds[10]
        self.assertEqual(2, player_rnd.player)
        self.assertEqual(26, np.sum(player_rnd.hands))
        self.assertEqual(10, player_rnd.nr_played_cards)
        self.assertEqual(2, player_rnd.nr_tricks)
        self.assertEqual(2, player_rnd.nr_cards_in_trick)
        self.assertEqual(S9, player_rnd.current_trick[0])
        self.assertEqual(S6, player_rnd.current_trick[1])
        self.assertEqual(29, player_rnd.points_team_0)
        self.assertEqual(0, player_rnd.points_team_1)

        player_rnd = player_rnds[11]
        self.assertEqual(1, player_rnd.player)
        self.assertEqual(25, np.sum(player_rnd.hands))
        self.assertEqual(11, player_rnd.nr_played_cards)
        self.assertEqual(2, player_rnd.nr_tricks)
        self.assertEqual(3, player_rnd.nr_cards_in_trick)
        self.assertEqual(S9, player_rnd.current_trick[0])
        self.assertEqual(S6, player_rnd.current_trick[1])
        self.assertEqual(SQ, player_rnd.current_trick[2])
        self.assertEqual(0, player_rnd.points_team_1)
        self.assertEqual(29, player_rnd.points_team_0)


if __name__ == '__main__':
    unittest.main()
