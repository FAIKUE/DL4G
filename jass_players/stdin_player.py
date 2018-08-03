from jass_base.game import Round
from jass_base.game_const import *
from jass_base.rule import Rule
from jass_players.player import Player


class StdinPlayer(Player):
    """StdinPlayer selects trump and plays the card which is chosen via stdin."""

    def play_card(self, rnd: Round) -> str:
        cards = rnd.current_trick.cards
        print("Your hand: %s" % convert_one_hot_encoded_cards_to_str_encoded_list(rnd.current_hand))
        if len(cards) > 0:
            print("Current Trick: %s" % (convert_int_encoded_cards_to_str_encoded(cards)))

        valid_cards = Rule.get_valid_cards(rnd.current_hand, cards, len(cards), rnd.trump)
        while True:
            card_str = input("> Enter Card [String] : ")
            if card_str not in card_strings:
                continue
            card = card_ids[card_str]
            if valid_cards[card] != 0:
                return card_str

    def select_trump(self, rnd: Round) -> int:
        possible_trumps = trump_strings_german_long.copy()
        if rnd.forehand:
            possible_trumps.append(trump_string_push_german)
        print("Possible trumps are: %s" % possible_trumps)
        trump_char = input("> Enter TRUMP [1 Char] : ")
        while True:
            if trump_char not in trump_strings_short:
                continue
            return trump_strings_short.index(trump_char)
