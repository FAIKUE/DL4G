import random

from jass_base.game import Round
from jass_base.game_const import *
from jass_base.rule import Rule
from jass_players.player import Player


class RandomPlayer(Player):
    """RandomPlayer chooses a random trump and plays a valid, but randomly chosen card."""

    def play_card(self, rnd: Round) -> str:
        cards = rnd.current_trick.cards
        valid_cards = Rule.get_valid_cards(rnd.current_hand, cards, len(cards), rnd.trump)  # 1-hot encoded
        valid_cards_str_list = convert_one_hot_encoded_cards_to_str_encoded_list(valid_cards)
        return random.choice(valid_cards_str_list)

    def select_trump(self, rnd: Round) -> int:
        possible_trump = trump_ints.copy()
        if rnd.forehand:
            possible_trump.append(PUSH)
        return random.choice(possible_trump)
