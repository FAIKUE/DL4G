import unittest
import logging
import numpy as np
from jass.base.const import JASS_HEARTS, next_player
from jass.arena.arena_cheating import ArenaCheating
from jass.base.player_round_cheating import PlayerRoundCheating
from jass.base.rule_hearts import RuleHearts
from jass.player.player_cheating import PlayerCheating
from jass.arena.trump_selection_none_strategy import TrumpNoneStrategy
from jass.arena.play_game_nr_rounds_strategy import PlayNrRoundsStrategy


class TestCheatingPlayer(PlayerCheating):
    def select_trump(self, rnd: PlayerRoundCheating) -> int or None:
        return None

    def play_card(self, rnd: PlayerRoundCheating) -> int:
        # check if we really got all information, i.e. the hand array is filled with sufficient values

        # how many cards should be in the hand that have not been played yet
        nr_cards_from_full_rounds = (9 - rnd.nr_tricks)
        cards_for_player = np.full(4, nr_cards_from_full_rounds)

        if rnd.nr_cards_in_trick > 0:
            # all players that have already played in the current round, now have one card less
            player = rnd.trick_first_player[rnd.nr_tricks]
            for i in range(rnd.nr_cards_in_trick):
                cards_for_player[player] -= 1
                player = next_player[player]

        # check that we got as many cards as we calculated
        for i in range(4):
            assert rnd.hands[i, :].sum() == cards_for_player[i]

        assert rnd.hand.sum() == cards_for_player[rnd.player]

        # we should put that in to the rnd, class, but lets test first
        rule = RuleHearts()
        valid_cards = rule.get_valid_cards_from_player_round(rnd)
        card = np.random.choice(np.flatnonzero(valid_cards))
        return card


class ArenaNrRoundsCheatingTestCase(unittest.TestCase):

    def test_arena(self):
        logging.basicConfig(level=logging.INFO)
        arena = ArenaCheating(jass_type=JASS_HEARTS,
                              trump_strategy=TrumpNoneStrategy(),
                              play_game_strategy=PlayNrRoundsStrategy(4))
        player = TestCheatingPlayer()

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
