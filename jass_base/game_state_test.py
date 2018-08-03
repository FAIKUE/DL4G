import json
import unittest

from data.log.log_parser import read_round

from jass_base.game_const import *
from jass_base.game_state import GameState
from jass_player_service.request_parser import PlayCardParser


class GameStateTestCase(unittest.TestCase):

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
        rnd = read_round(round_dict)
        game_stats = GameState.get_game_states(rnd)
        self.assertEqual(36, len(game_stats))

        # check properties for all moves
        for gs in game_stats:
            self.assertEqual(5, gs.trump)
            self.assertEqual(3, gs.dealer)
            self.assertEqual(0, gs.declared_trump)
            self.assertEqual(False, gs.forehand)

        # first trick
        gs = game_stats[0]
        self.assertEqual(2, gs.current_player)
        self.assertEqual(9, np.sum(gs.hand))
        self.assertEqual(0, gs.nr_cards_played)
        self.assertEqual(C7, gs.card_played)
        self.assertEqual(0, gs.nr_tricks_played)
        self.assertEqual([], gs.cards_played_in_trick)
        self.assertTrue(np.all(gs.cards_played_in_round[0] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[1] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[2] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[3] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.hand == get_cards_encoded([C7, SA, SQ, HJ, C9, DJ, CQ, DK, C8])))
        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[1]
        self.assertEqual(1, gs.current_player)
        self.assertEqual(9, np.sum(gs.hand))
        self.assertEqual(1, gs.nr_cards_played)
        self.assertEqual(CK, gs.card_played, CK)
        self.assertEqual(0, gs.nr_tricks_played, 0)
        self.assertEqual([C7], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[2]
        self.assertEqual(0, gs.current_player, 0)
        self.assertEqual(9, np.sum(gs.hand), 9)
        self.assertEqual(2, gs.nr_cards_played)
        self.assertEqual(C6, gs.card_played, C6)
        self.assertEqual(0, gs.nr_tricks_played, 0)
        self.assertEqual([C7, CK],gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[3]
        self.assertEqual(3, gs.current_player)
        self.assertEqual(9, np.sum(gs.hand))
        self.assertEqual(3, gs.nr_cards_played)
        self.assertEqual(CJ, gs.card_played)
        self.assertEqual(0, gs.nr_tricks_played)
        self.assertTrue([C6, C7, CK], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        # second trick
        gs = game_stats[4]
        self.assertEqual(0, gs.current_player)
        self.assertEqual(8, np.sum(gs.hand))
        self.assertEqual(0, gs.nr_cards_played)
        self.assertEqual(S7, gs.card_played)
        self.assertEqual(1, gs.nr_tricks_played)
        self.assertTrue(np.all(gs.cards_played_in_round[0] == get_cards_encoded([C6])))
        self.assertTrue(np.all(gs.cards_played_in_round[1] == get_cards_encoded([CK])))
        self.assertTrue(np.all(gs.cards_played_in_round[2] == get_cards_encoded([C7])))
        self.assertTrue(np.all(gs.cards_played_in_round[3] == get_cards_encoded([CJ])))
        self.assertTrue(np.all(np.sum(gs.cards_played_in_round, axis=0) == get_cards_encoded([C6, C7, CJ, CK])))
        self.assertEqual(17, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[5]
        self.assertEqual(3, gs.current_player)
        self.assertEqual(8, np.sum(gs.hand))
        self.assertEqual(1, gs.nr_cards_played)
        self.assertEqual(SJ, gs.card_played, SJ)
        self.assertEqual(1, gs.nr_tricks_played, 1)
        self.assertEqual([S7], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(17, gs.points_opponent)

        gs = game_stats[6]
        self.assertEqual(2, gs.current_player, 2)
        self.assertEqual(8, np.sum(gs.hand), 8)
        self.assertEqual(2, gs.nr_cards_played, 2)
        self.assertEqual(SA, gs.card_played, SA)
        self.assertEqual(1, gs.nr_tricks_played, 1)
        self.assertEqual([S7, SJ], gs.cards_played_in_trick)
        self.assertEqual(17, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[7]
        self.assertEqual(1, gs.current_player, 1)
        self.assertEqual(8, np.sum(gs.hand), 8)
        self.assertEqual(3, gs.nr_cards_played, 3)
        self.assertEqual(C10, gs.card_played, C10)
        self.assertEqual(1, gs.nr_tricks_played, 1)
        self.assertEqual([S7, SJ, SA], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(17, gs.points_opponent)

        # third trick
        gs = game_stats[8]
        self.assertEqual(0, gs.current_player)
        self.assertEqual(7, np.sum(gs.hand))
        self.assertEqual(0, gs.nr_cards_played)
        self.assertEqual(S9, gs.card_played)
        self.assertEqual(2, gs.nr_tricks_played)
        self.assertTrue(np.all(gs.cards_played_in_round[0] == get_cards_encoded([C6, S7])))
        self.assertTrue(np.all(gs.cards_played_in_round[1] == get_cards_encoded([CK, C10])))
        self.assertTrue(np.all(gs.cards_played_in_round[2] == get_cards_encoded([C7, SA])))
        self.assertTrue(np.all(gs.cards_played_in_round[3] == get_cards_encoded([CJ, SJ])))
        self.assertTrue(np.all(np.sum(gs.cards_played_in_round, axis=0) ==
                               get_cards_encoded([C6, C7, CJ, CK, S7, C10, SA, SJ])))
        self.assertEqual([], gs.cards_played_in_trick)
        self.assertEqual(29, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[9]
        self.assertEqual(3, gs.current_player)
        self.assertEqual(7, np.sum(gs.hand))
        self.assertEqual(1, gs.nr_cards_played)
        self.assertEqual(S6, gs.card_played, S6)
        self.assertEqual(2, gs.nr_tricks_played)
        self.assertEqual([S9], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(29, gs.points_opponent)

        gs = game_stats[10]
        self.assertEqual(2, gs.current_player)
        self.assertEqual(7, np.sum(gs.hand))
        self.assertEqual(2, gs.nr_cards_played)
        self.assertEqual(SQ, gs.card_played, SQ)
        self.assertEqual(2, gs.nr_tricks_played)
        self.assertEqual([S9, S6], gs.cards_played_in_trick)
        self.assertEqual(29, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        gs = game_stats[11]
        self.assertEqual(1, gs.current_player)
        self.assertEqual(7, np.sum(gs.hand))
        self.assertEqual(3, gs.nr_cards_played)
        self.assertEqual(D10, gs.card_played)
        self.assertEqual(2, gs.nr_tricks_played)
        self.assertEqual([S9, S6, SQ], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(29, gs.points_opponent)

    def test_normalize(self):
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
        rnd = read_round(round_dict)
        game_stats = GameState.get_game_states(rnd)
        self.assertEqual(36, len(game_stats))

        # check properties for all moves
        for gs in game_stats:
            self.assertEqual(5, gs.trump)
            self.assertEqual(3, gs.dealer)
            self.assertEqual(0, gs.declared_trump)
            self.assertEqual(False, gs.forehand)

        # first trick
        gs = game_stats[0]
        self.assertEqual(2, gs.current_player)
        self.assertEqual(9, np.sum(gs.hand))
        self.assertEqual(0, gs.nr_cards_played)
        self.assertEqual(C7, gs.card_played)
        self.assertEqual(0, gs.nr_tricks_played)
        self.assertEqual([], gs.cards_played_in_trick)
        self.assertTrue(np.all(gs.cards_played_in_round[0] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[1] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[2] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.cards_played_in_round[3] == get_cards_encoded([])))
        self.assertTrue(np.all(gs.hand == get_cards_encoded([C7, SA, SQ, HJ, C9, DJ, CQ, DK, C8])))
        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)

        # normalize and check again
        gs_norm = GameState.normalize(gs)
        self.assertEqual(0, gs_norm.current_player)
        self.assertEqual(5, gs_norm.trump)
        self.assertEqual(1, gs_norm.dealer)
        self.assertEqual(2, gs_norm.declared_trump)
        self.assertEqual(9, np.sum(gs_norm.hand))
        self.assertEqual(0, gs_norm.nr_cards_played)
        self.assertEqual(0, gs_norm.nr_tricks_played)
        self.assertEqual([], gs_norm.cards_played_in_trick)
        self.assertTrue(np.all(gs_norm.cards_played_in_round[0] == get_cards_encoded([])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[1] == get_cards_encoded([])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[2] == get_cards_encoded([])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[3] == get_cards_encoded([])))
        self.assertTrue(np.all(gs_norm.hand == get_cards_encoded([C7, SA, SQ, HJ, C9, DJ, CQ, DK, C8])))
        self.assertEqual(0, gs_norm.points_own)
        self.assertEqual(0, gs_norm.points_opponent)

        # same for another player and round
        gs = game_stats[11]
        self.assertEqual(1, gs.current_player)
        self.assertEqual(7, np.sum(gs.hand))
        self.assertEqual(3, gs.nr_cards_played)
        self.assertEqual(D10, gs.card_played)
        self.assertEqual(2, gs.nr_tricks_played)
        self.assertEqual([S9, S6, SQ], gs.cards_played_in_trick)
        self.assertEqual(0, gs.points_own)
        self.assertEqual(29, gs.points_opponent)
        self.assertTrue(np.all(gs.cards_played_in_round[0] == get_cards_encoded([C6, S7])))
        self.assertTrue(np.all(gs.cards_played_in_round[1] == get_cards_encoded([CK, C10])))
        self.assertTrue(np.all(gs.cards_played_in_round[2] == get_cards_encoded([C7, SA])))
        self.assertTrue(np.all(gs.cards_played_in_round[3] == get_cards_encoded([CJ, SJ])))

        gs_norm = GameState.normalize(gs)
        self.assertEqual(0, gs_norm.current_player)
        self.assertEqual(7, np.sum(gs_norm.hand))
        self.assertEqual(3, gs_norm.nr_cards_played)
        self.assertEqual(D10, gs_norm.card_played)
        self.assertEqual(2, gs_norm.nr_tricks_played)
        self.assertEqual([S9, S6, SQ], gs_norm.cards_played_in_trick)
        self.assertEqual(0, gs_norm.points_own)
        self.assertEqual(29, gs_norm.points_opponent)

        self.assertTrue(np.all(gs_norm.cards_played_in_round[3] == get_cards_encoded([C6, S7])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[0] == get_cards_encoded([CK, C10])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[1] == get_cards_encoded([C7, SA])))
        self.assertTrue(np.all(gs_norm.cards_played_in_round[2] == get_cards_encoded([CJ, SJ])))

    def test_get_latest_game_state_middle(self):
        round_string = '{"trump":4,"dealer":3,"tss":1,"tricks":[' \
                       '{"cards":["SA","S7","SQ","S6"],"points":14,"win":2,"first":2},' \
                       '{"cards":["C8","CJ","CQ","CK"],"points":17,"win":3,"first":2},' \
                       '{"cards":["D6","D7","DJ","DA"],"points":13,"win":0,"first":3},' \
                       '{"cards":["HA","H6"],"points":0,"win":0,"first":0}],' \
                       '"player":[{"hand":[]},{"hand":[]},' \
                       '{"hand":["S8","S9","SK","CA","C10","H9"]},{"hand":[]}],' \
                       '"jassTyp":"SCHIEBER_2500"}'
        # we use the parser, as it already can read incomplete rounds, while the read_round expects a full round
        play_card_parser = PlayCardParser(round_string)
        self.assertTrue(play_card_parser.is_valid_request())
        rnd = play_card_parser.get_parsed_round()

        gs = GameState.get_last_game_state(rnd)


        self.assertEqual(2, gs.current_player)
        self.assertEqual(3, gs.dealer)
        self.assertEqual(0, gs.declared_trump)
        self.assertEqual(4, gs.trump)
        self.assertFalse(gs.forehand)
        self.assertEqual(3, gs.nr_tricks_played)
        self.assertEqual([HA, H6], gs.cards_played_in_trick)

        # cards played by each player
        expected_played_0 = get_cards_encoded([SQ, CQ, DA])
        expected_played_1 = get_cards_encoded([S7, CJ, DJ])
        expected_played_2 = get_cards_encoded([SA, C8, D7])
        expected_played_3 = get_cards_encoded([S6, CK, D6])

        expected_played = np.stack([expected_played_0, expected_played_1, expected_played_2, expected_played_3])

        self.assertTrue(np.all(expected_played == gs.cards_played_in_round))

        self.assertEqual(27, gs.points_own)
        self.assertEqual(17, gs.points_opponent)
        self.assertEqual(2, gs.nr_cards_played)

        expected_hand = [S8, S9, SK, CA, C10, H9]
        self.assertTrue(np.all(get_cards_encoded(expected_hand) == gs.hand))

    def test_get_latest_game_state_first_trick(self):
        request_data = '{"trump":0,"dealer":3,"tss":0,"tricks":[' \
                       '{"cards":["DJ","D7","D10"],"points":0,"win":0,"first":0}],' \
                       '"player":[{"hand":[]},{"hand":[]},{"hand":[]},' \
                       '{"hand":["S6","S7","S8","C6","C7","C8","D6","D8","HJ"]}],' \
                       '"jassTyp":"SCHIEBER_1000"}'
        play_card_parser = PlayCardParser(request_data)
        self.assertTrue(play_card_parser.is_valid_request())
        rnd = play_card_parser.get_parsed_round()

        gs = GameState.get_last_game_state(rnd)

        self.assertEqual(1, gs.current_player)
        self.assertEqual(3, gs.dealer)
        self.assertEqual(2, gs.declared_trump)
        self.assertEqual(0, gs.trump)
        self.assertTrue(gs.forehand)
        self.assertEqual(0, gs.nr_tricks_played)
        self.assertEqual([DJ, D7, D10], gs.cards_played_in_trick)

        # cards played by each player
        expected_played_0 = get_cards_encoded([])
        expected_played_1 = get_cards_encoded([])
        expected_played_2 = get_cards_encoded([])
        expected_played_3 = get_cards_encoded([])

        expected_played = np.stack([expected_played_0, expected_played_1, expected_played_2, expected_played_3])

        self.assertTrue(np.all(expected_played == gs.cards_played_in_round))

        self.assertEqual(0, gs.points_own)
        self.assertEqual(0, gs.points_opponent)
        self.assertEqual(3, gs.nr_cards_played)

        expected_hand = [S6, S7, S8, C6, C7, C8, D6, D8, HJ]
        self.assertTrue(np.all(get_cards_encoded(expected_hand) == gs.hand))

    def test_get_latest_game_state_last_trick(self):
        request_data = '{"trump":2,"dealer":2,"tss":1,"tricks":[' \
                       '{"cards":["SJ","S8","S6","S7"],"points":20,"win":1,"first":1},' \
                       '{"cards":["S9","S10","SQ","SK"],"points":31,"win":1,"first":1},' \
                       '{"cards":["CJ","CA","C6","C10"],"points":23,"win":0,"first":1},' \
                       '{"cards":["C8","C7","D7","CK"],"points":4,"win":1,"first":0},' \
                       '{"cards":["H8","HJ","H6","HA"],"points":13,"win":2,"first":1},' \
                       '{"cards":["DJ","DQ","D6","DA"],"points":16,"win":3,"first":2},' \
                       '{"cards":["CQ","H10","D10","C9"],"points":23,"win":3,"first":3},' \
                       '{"cards":["H7","HQ","HK","D8"],"points":7,"win":1,"first":3},' \
                       '{"cards":["SA","D9","H9"],"points":0,"win":0,"first":1}],' \
                       '"player":[{"hand":[]},{"hand":[]},{"hand":[]},{"hand":["DK"]}],"jassTyp":"SCHIEBER_2500"}'
        play_card_parser = PlayCardParser(request_data)
        self.assertTrue(play_card_parser.is_valid_request())
        rnd = play_card_parser.get_parsed_round()

        gs = GameState.get_last_game_state(rnd)

        self.assertEqual(2, gs.current_player)
        self.assertEqual(2, gs.dealer)
        self.assertEqual(3, gs.declared_trump)
        self.assertEqual(2, gs.trump)
        self.assertFalse(gs.forehand)
        self.assertEqual(8, gs.nr_tricks_played)
        self.assertEqual([SA, D9, H9], gs.cards_played_in_trick)

        # cards played by each player
        expected_played_0 = get_cards_encoded([S8, S10, CA, C8, HJ, D6, C9, D8])
        expected_played_1 = get_cards_encoded([SJ, S9, CJ, CK, H8, DQ, D10, HK])
        expected_played_2 = get_cards_encoded([S7, SK, C10, D7, HA, DJ, H10, HQ])
        expected_played_3 = get_cards_encoded([S6, SQ, C6, C7, H6, DA, CQ, H7])

        expected_played = np.stack([expected_played_0, expected_played_1, expected_played_2, expected_played_3])

        self.assertTrue(np.all(expected_played == gs.cards_played_in_round))

        self.assertEqual(36, gs.points_own)
        self.assertEqual(101, gs.points_opponent)
        self.assertEqual(3, gs.nr_cards_played)

        expected_hand = [DK]
        self.assertTrue(np.all(get_cards_encoded(expected_hand) == gs.hand))


if __name__ == '__main__':
    unittest.main()
