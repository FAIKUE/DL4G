import logging
from source.jass.base.player_round import PlayerRound
from source.jass.base.const import *
from source.jass.player.player import Player


class RandomPlayerHearts(Player):
    """RandomPlayer chooses a random valid trump and plays a valid, but randomly chosen card."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def select_trump(self, rnd: PlayerRound) -> int or None:
        return None

    def play_card(self, player_rnd: PlayerRound) -> int:
        valid_cards = player_rnd.get_valid_cards()
        card = np.random.choice(np.flatnonzero(valid_cards))
        self._logger.debug('Played card: {}'.format(card_strings[card]))
        return card
