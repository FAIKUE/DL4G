import random

from jass.base.player_round import PlayerRound
from jass.base.const import *
from jass.player.player import Player
from jass.base.rule import Rule


class RandomPlayer(Player):
    """RandomPlayer chooses a random valid trump and plays a valid, but randomly chosen card."""

    def select_trump(self, rnd: PlayerRound) -> int:
        possible_trump = trump_ints.copy()
        if rnd.forehand:
            possible_trump.append(PUSH)
        return random.choice(possible_trump)

    def play_card(self, player_rnd: PlayerRound) -> int:
        valid_cards = Rule.get_valid_cards_from_player_round(player_rnd)
        return np.random.choice(np.flatnonzero(valid_cards))
