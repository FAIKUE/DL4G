import random

import logging
from jass.base.player_round import PlayerRound
from jass.base.const import *
from jass.player.player import Player
from jass.base.rule_schieber import RuleSchieber


class RandomPlayerSchieber(Player):
    """RandomPlayer chooses a random valid trump and plays a valid, but randomly chosen card."""
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._rule = RuleSchieber()

    def select_trump(self, rnd: PlayerRound) -> int:
        possible_trump = trump_ints.copy()
        if rnd.forehand:
            possible_trump.append(PUSH)
        return random.choice(possible_trump)

    def play_card(self, player_rnd: PlayerRound) -> int:
        valid_cards = player_rnd.get_valid_cards()
        card = np.random.choice(np.flatnonzero(valid_cards))
        self._logger.debug('Played card: {}'.format(card_strings[card]))
        return card
