import unittest
from jass.arena.arena_nr_rounds import ArenaNrRounds
from jass.player.random_player import RandomPlayer


class ArenaNrRoundsTestCase(unittest.TestCase):

    def test_arena(self):
        arena = ArenaNrRounds()
        player = RandomPlayer()

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
