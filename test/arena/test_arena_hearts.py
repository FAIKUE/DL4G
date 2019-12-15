import unittest
import logging
from source.jass.base.const import JASS_HEARTS
from source.jass.arena.arena import Arena
from source.jass.arena.trump_selection_none_strategy import TrumpNoneStrategy
from source.jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy
from source.jass.player.random_player_hearts import RandomPlayerHearts


class ArenaNrRoundsTestCase(unittest.TestCase):

    def test_arena(self):
        logging.basicConfig(level=logging.INFO)
        arena = Arena(jass_type=JASS_HEARTS,
                      trump_strategy=TrumpNoneStrategy(),
                      play_game_strategy=PlayNrRoundsStrategy(4))
        player = RandomPlayerHearts()

        arena.set_players(player, player, player, player)
        arena.nr_games_to_play = 10
        arena.play_all_games()

        self.assertEqual(10, arena.nr_games_played)
        self.assertEqual(arena.nr_wins_team_0 + arena.nr_wins_team_1 + arena.nr_draws, arena.nr_games_played)
        print(arena.nr_wins_team_0)
        print(arena.nr_wins_team_1)
        print(arena.delta_points)


if __name__ == '__main__':
    unittest.main()
