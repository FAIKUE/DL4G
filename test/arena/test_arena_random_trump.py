import unittest
from source.jass.base.const import JASS_SCHIEBER_1000
from source.jass.arena.arena import Arena
from source.jass.arena.trump_selection_random_strategy import TrumpRandomStrategy
from source.jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy
from source.jass.player.random_player_schieber import RandomPlayerSchieber


class ArenaRandomTrumpTestCase(unittest.TestCase):

    def test_arena(self):
        arena = Arena(jass_type=JASS_SCHIEBER_1000,
                      trump_strategy=TrumpRandomStrategy(),
                      play_game_strategy=PlayNrRoundsStrategy(10))
        player = RandomPlayerSchieber()

        arena.set_players(player, player, player, player)
        arena.nr_games_to_play = 2
        arena.play_all_games()

        self.assertEqual(2, arena.nr_games_played)
        self.assertEqual(arena.nr_wins_team_0 + arena.nr_wins_team_1 + arena.nr_draws, arena.nr_games_played)
        print(arena.nr_wins_team_0)
        print(arena.nr_wins_team_1)
        print(arena.delta_points)


if __name__ == '__main__':
    unittest.main()
