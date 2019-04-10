import unittest

from jass.base.const import *
from jass.base.round_schieber import RoundSchieber
from jass.io.player_round_log_generator import PlayerRoundLogGenerator


class PlayerRoundLogGeneratorCase(unittest.TestCase):

    PLAYER_IDS = [10, 20, 30, 40]

    def test_round_to_player_round_returns_36_elements(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)

        self.assertEqual(36, len(player_rounds))

    def test_4_rounds_return_144_elements(self):
        rnds = self.get_multiple_identical_rounds(4)

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._rounds_to_player_rounds(rnds)

        self.assertEqual(144, len(player_rounds))

    def test_dict_sets_dealer(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(WEST, result["dealer"])

    def test_dict_sets_trump_declarer(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(result["declaredtrump"], NORTH)

    def test_dict_sets_trump(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(U, result["trump"])

    def test_dict_sets_forehand(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(False, result["forehand"])

    def test_dict_sets_points(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[25])

        self.assertEqual(29, result["pointsteamown"])
        self.assertEqual(60, result["pointsteamopponent"])

    def test_dict_sets_nrplayedcards(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[25])

        self.assertEqual(25, result["nrplayedcards"])

    def test_dict_sets_player(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(SOUTH, result["player"])

    def test_dict_sets_hand_with_9_cards_in_first_round(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[0])

        self.assertEqual(9, len(result["hand"]))

    def test_dict_sets_hand_with_1_cards_in_34_playerround(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[34])

        self.assertEqual(1, len(result["hand"]))

    def test_dict_sets_nrcardsplayed(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[3])

        self.assertEqual(3, result["nrcardsintrick"])

    def test_dict_sets_currenttrick(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[3])
        result2 = testee._dict_from_round(player_rounds[4])

        self.assertListEqual(['C7', 'CK', 'C6'], result["currenttrick"])

    def test_dict_sets_tricks(self):
        rnd = self.get_round()

        testee = PlayerRoundLogGenerator("", "")
        player_rounds = testee._round_to_player_rounds(rnd)
        result = testee._dict_from_round(player_rounds[14])

        self.assertEqual(3, len(result["tricks"]))
        self.assertEqual(SOUTH, result["tricks"][0]["first"])
        self.assertListEqual(["C7", "CK", "C6", "CJ"], list(result["tricks"][0]["cards"]))
        self.assertEqual(result["tricks"][0]["win"], result["tricks"][1]["first"])
        self.assertEqual(result["tricks"][1]["win"], result["tricks"][2]["first"])

    def test_first_trick_has_empty_currenttrick(self):
        rnd = self.get_multiple_identical_rounds(5)

        testee = PlayerRoundLogGenerator("", "")
        result = testee._rounds_to_player_rounds_dict(rnd)

        self.assertListEqual([], result[0]["currenttrick"])

    def test_fifth_trick_has_empty_currenttrick(self):
        rnd = self.get_multiple_identical_rounds(5)

        testee = PlayerRoundLogGenerator("", "")
        result = testee._rounds_to_player_rounds_dict(rnd)

        self.assertListEqual([], result[4]["currenttrick"])

    def _test_writefile(self):
        rnd = self.get_multiple_identical_rounds(3)

        testee = PlayerRoundLogGenerator("", "")
        result = testee._rounds_to_player_rounds_dict(rnd)
        testee._generate_logs(result, "..\\test_results\\test.json")

    def _test_log_to_playerroundlog(self):
        testee = PlayerRoundLogGenerator("", "")
        testee._generate_from_file("..\\resources\\small_log.txt", "..\\test_results")

    def get_round(self):
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
        rnd.assert_invariants()
        return dict(round=rnd, players=[20, 30, 40, 50])

    def get_multiple_identical_rounds(self, number_of_rounds: int):
        rounds_to_return = []
        for i in range(0, number_of_rounds):
            rounds_to_return.append(self.get_round())

        return rounds_to_return


if __name__ == '__main__':
    unittest.main()
