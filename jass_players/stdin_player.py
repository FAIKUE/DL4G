from jass_base.game import Round
from jass_base.game_const import *
from jass_base.rule import Rule
from jass_players.player import Player


class StdinPlayer(Player):
    """StdinPlayer selects trump and plays the card which is chosen via stdin."""

    def select_trump(self, rnd: Round) -> int:
        possible_trumps = trump_strings_german_long.copy()
        if rnd.forehand:
            possible_trumps.append(trump_string_push_german)
        print("Your hand: %s" % convert_one_hot_encoded_cards_to_str_encoded_list(rnd.current_hand))
        print("Possible trumps are: %s" % possible_trumps)
        while True:
            trump_char = input("> Enter trump [1 char] : ").upper()
            if trump_char not in trump_strings_short:
                print("'%s' is no valid trump to select" % trump_char)
                continue
            return trump_strings_short.index(trump_char)

    def play_card(self, rnd: Round) -> str:
        cards = rnd.current_trick.cards
        print("Your hand: %s" % convert_one_hot_encoded_cards_to_str_encoded_list(rnd.current_hand))
        trump_and_trick = "Trump: " + trump_strings_german_long[rnd.trump]
        if len(cards) > 0:
            trump_and_trick = trump_and_trick +\
                              ", current trick: %s" % convert_int_encoded_cards_to_str_encoded(cards)
        print(trump_and_trick)

        valid_cards = Rule.get_valid_cards(rnd.current_hand, cards, len(cards), rnd.trump)
        while True:
            card_str = input("> Enter card [string] : ").upper()
            if card_str not in card_strings:
                print("'%s' is not a card you have in your hand." % card_str)
                continue
            card = card_ids[card_str]
            if valid_cards[card] != 0:
                return card_str
            else:
                print("'%s' is not a valid card to play." % card_str)
