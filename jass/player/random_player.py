import random

from jass.base.player_round import PlayerRound
from jass.base.const import *
from jass.player.player import Player
# TODO: move Rule to new jass.base package.
from jass_base.rule import Rule


class RandomPlayer(Player):
    """RandomPlayer chooses a random valid trump and plays a valid, but randomly chosen card."""

    def select_trump(self, rnd: PlayerRound) -> int:
        possible_trump = trump_ints.copy()
        if rnd.forehand:
            possible_trump.append(PUSH)
        return random.choice(possible_trump)

    def play_card(self, rnd: PlayerRound) -> str:
        trick_cards = convert_one_hot_encoded_cards_to_int_encoded_list(rnd.get_current_trick())
        valid_cards = Rule.get_valid_cards(rnd.hand, trick_cards, len(trick_cards), rnd.trump)  # 1-hot encoded
        valid_cards_str_list = convert_one_hot_encoded_cards_to_str_encoded_list(valid_cards)
        return random.choice(valid_cards_str_list)
