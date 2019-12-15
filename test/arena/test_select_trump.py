import unittest
from source.jass.base.const import JASS_SCHIEBER_1000, PUSH, SA
from source.jass.arena.arena import Arena
from source.jass.arena.trump_selection_players_strategy import TrumpPlayerStrategy
from source.jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy
from source.jass.base.player_round import PlayerRound
from source.jass.player.player import Player


class ArenaNrRoundsTestCase(unittest.TestCase):

    def test_invalid_trump_double_push(self):
        arena = Arena(jass_type=JASS_SCHIEBER_1000,
                      trump_strategy=TrumpPlayerStrategy(),
                      play_game_strategy=PlayNrRoundsStrategy(4))
        fix_trump_player = FixTestPlayer(PUSH, SA)

        arena.set_players(fix_trump_player, fix_trump_player, fix_trump_player, fix_trump_player)
        arena.nr_games_to_play = 2
        self.assertRaises(RuntimeError, arena.play_all_games)

    def test_invalid_trump_negative_number(self):
        arena = Arena(jass_type=JASS_SCHIEBER_1000,
                      trump_strategy=TrumpPlayerStrategy(),
                      play_game_strategy=PlayNrRoundsStrategy(4))
        fix_trump_player = FixTestPlayer(-1, SA)

        arena.set_players(fix_trump_player, fix_trump_player, fix_trump_player, fix_trump_player)
        arena.nr_games_to_play = 2
        self.assertRaises(RuntimeError, arena.play_all_games)

    def test_invalid_trump_8(self):
        arena = Arena(jass_type=JASS_SCHIEBER_1000,
                      trump_strategy=TrumpPlayerStrategy(),
                      play_game_strategy=PlayNrRoundsStrategy(4))
        fix_trump_player = FixTestPlayer(8, SA)

        arena.set_players(fix_trump_player, fix_trump_player, fix_trump_player, fix_trump_player)
        arena.nr_games_to_play = 2
        self.assertRaises(RuntimeError, arena.play_all_games)

if __name__ == '__main__':
    unittest.main()


class FixTestPlayer(Player):
    """FixTestPlayer returns always the same trump and card to play.
       ---> FOR TEST PURPOSES ONLY!!! <---"""
    def __init__(self, trump: int, card: int):
        self._trump = trump
        self._card = card

    def select_trump(self, rnd: PlayerRound) -> int:
        return self._trump

    def play_card(self, player_rnd: PlayerRound) -> int:
        return self._card
