from jass.base.const import *
from jass.player.player import Player
from jass.base.player_round import PlayerRound
from jass.base.rule import Rule


class StdinPlayer(Player):
    """StdinPlayer selects trump and plays the card which is entered by the user via stdin."""

    def select_trump(self, rnd: PlayerRound) -> int:
        possible_trumps = trump_strings_german_long.copy()
        if rnd.forehand:
            possible_trumps.append(trump_string_push_german)
        print("Your hand: %s" % convert_one_hot_encoded_cards_to_str_encoded_list(rnd.hand))
        print("Possible trumps are: %s" % possible_trumps)
        while True:
            trump_char = input("> Enter trump [1 char] : ").upper()
            if trump_char not in trump_strings_short:
                print("'%s' is no valid trump to select" % trump_char)
                continue
            return trump_strings_short.index(trump_char)

    def play_card(self, rnd: PlayerRound) -> int:
        trick_cards = convert_one_hot_encoded_cards_to_int_encoded_list(rnd.get_current_trick())
        print("Your hand: %s" % convert_one_hot_encoded_cards_to_str_encoded_list(rnd.hand))
        trump_and_trick = "Trump: '%s'" % trump_strings_german_long[rnd.trump]
        if len(trick_cards) > 0:
            trump_and_trick = trump_and_trick +\
                              ", current trick: %s" % convert_int_encoded_cards_to_str_encoded(trick_cards)
        print(trump_and_trick)

        valid_cards = Rule.get_valid_cards(rnd.hand, trick_cards, len(trick_cards), rnd.trump)  # 1-hot encoded
        while True:
            card_str = input("> Enter card to play [string] : ").upper()
            if card_str not in card_strings:
                print("'%s' is not a card you have in your hand." % card_str)
                continue
            card = card_ids[card_str]
            if valid_cards[card] != 0:
                return card
            else:
                print("'%s' is not a valid card to play." % card_str)
