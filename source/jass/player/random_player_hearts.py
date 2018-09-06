import logging
from jass.base.player_round import PlayerRound
from jass.base.const import *
from jass.player.player import Player
from jass.base.rule_hearts import RuleHearts


class RandomPlayerHearts(Player):
    """RandomPlayer chooses a random valid trump and plays a valid, but randomly chosen card."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._rule = RuleHearts()

    def select_trump(self, rnd: PlayerRound) -> int or None:
        return None

    def play_card(self, player_rnd: PlayerRound) -> int:
        valid_cards = self._rule.get_valid_cards_from_player_round(player_rnd)
        card = np.random.choice(np.flatnonzero(valid_cards))
        self._logger.debug('Played card: {}'.format(card_strings[card]))
        return card
