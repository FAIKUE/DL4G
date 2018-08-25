# HSLU
#
# Created by Thomas Koller on 22.08.18
#
"""
Generate json document for Jass player service
"""
import json
import numpy as np
from jass.base.player_round import PlayerRound
from jass.base.const import *


class PlayerRoundRequestGenerator:
    """
    Generate the appropriate request for a specific PlayerRound that can be used for the player service
    """
    @staticmethod
    def generate_dict(player_rnd: PlayerRound) -> dict:
        """
        Generate dict for the player round that corresponds to the json sp[ecification of the interface
        Args:
            player_rnd: the player round to convert

        Returns:
            dict representation of the player round
        """
        data = dict()

        data['dealer'] = int(player_rnd.dealer)
        # optional fields

        # tss only needs to be present if its value is 1
        if player_rnd.forehand is False:
            data['tss'] = 1

        if player_rnd.trump is not None:
            data['trump'] = int(player_rnd.trump)

        # played tricks
        tricks = []

        # full tricks
        for i in range(player_rnd.nr_tricks):
            # cards of tricks
            cards_int = player_rnd.tricks[i,:].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(cards_int)
            trick = dict(
                cards=cards,
                points=int(player_rnd.trick_points[i]),
                win=int(player_rnd.trick_winner[i]),
                first=int(player_rnd.trick_first_player[i]))
            tricks.append(trick)
        # add last (current) trick even if empty
        if player_rnd.nr_cards_in_trick > 0:
            cards_int = player_rnd.current_trick[0:player_rnd.nr_cards_in_trick].tolist()
            cards = convert_int_encoded_cards_to_str_encoded(cards_int)
        else:
            cards = []
        trick = dict(
            cards=cards,
            first=int(player_rnd.trick_first_player[player_rnd.nr_tricks])
        )
        tricks.append(trick)
        data['tricks'] = tricks

        # hand of player
        hand_empty = dict(hand=[])
        player = [hand_empty, hand_empty, hand_empty, hand_empty]
        hand = dict(hand=convert_one_hot_encoded_cards_to_str_encoded_list(player_rnd.hand))
        player[player_rnd.player] = hand
        data['player'] = player

        # we
        data['jassTyp'] = "SCHIEBER_1000"

        return data

    @staticmethod
    def generate_json(player_rnd: PlayerRound) -> str:
        """
        Generate json representation for the player round (from the dict).
        Args:
            player_rnd:

        Returns:
            json representation of the player round
        """
        data = PlayerRoundRequestGenerator.generate_dict(player_rnd)
        return json.dumps(data)
