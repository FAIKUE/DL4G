import logging
import json

from jass.base.const import card_ids
from jass.base.player_round import PlayerRound

import numpy as np

from jass.base.player_round_cheating import PlayerRoundCheating


class PlayerRoundLogParser:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def parse_rounds_from_file(self, filename) -> [PlayerRound]:
        file = open(filename)
        player_rounds = []
        try:
            for line in file:
                round_dict = json.loads(line)
                rnd = self.initialize_round(round_dict)
                rnd = self.add_round_information(rnd, round_dict)
                player_rounds.append(rnd)
        finally:
            file.close()

        return player_rounds

    def parse_cheating_rounds_from_file(self, filename) -> [PlayerRoundCheating]:
        file = open(filename)
        player_rounds = []
        try:
            for line in file:
                round_dict = json.loads(line)
                rnd = self.initialize_round_cheating(round_dict)
                rnd = self.add_round_information(rnd, round_dict)
                rnd = self.add_cheating_information(rnd, round_dict)
                player_rounds.append(rnd)
        finally:
            file.close()

        return player_rounds

    def initialize_round_cheating(self, round_dict):
        rnd = PlayerRoundCheating(
            dealer=round_dict['dealer'],
            player=round_dict['player'],
            trump=round_dict['trump'],
            forehand=round_dict['forehand'],
            declared_trump=round_dict['declaredtrump'],
            jass_type=round_dict['jassTyp'],
            rule=None
        )

        return rnd

    def initialize_round(self, round_dict):
        rnd = PlayerRound(
            dealer=round_dict['dealer'],
            player=round_dict['player'],
            trump=round_dict['trump'],
            forehand=round_dict['forehand'],
            declared_trump=round_dict['declaredtrump'],
            jass_type=round_dict['jassTyp'],
            rule=None
        )

        return rnd

    def add_round_information(self, rnd, round_dict):
        tricks = round_dict['tricks']
        for i, trick in enumerate(tricks):
            cards = self.get_id_trick_from_constants(trick["cards"])
            points = trick["points"]
            win = trick["win"]
            first = trick["first"]
            rnd.tricks[i] = cards
            rnd.trick_winner[i] = win
            rnd.trick_points[i] = points
            rnd.trick_first_player[i] = first

        rnd.current_trick = self.get_id_trick_from_constants(round_dict['currenttrick'])
        rnd.nr_cards_in_trick = len(round_dict['currenttrick'])
        rnd.nr_played_cards = round_dict['nrplayedcards']
        rnd.nr_tricks = len(tricks)
        for card_constant in round_dict['hand']:
            rnd.hand[card_ids[card_constant]] = 1

        return rnd

    def get_id_trick_from_constants(self, constant_trick):
        cards = [card_ids[card] for card in constant_trick]
        while len(cards) < 4:
            cards.append(-1)

        return np.array(cards)

    def add_cheating_information(self, rnd, round_dict):
        for i, hand in enumerate(round_dict['hands']):
            for card_constant in hand:
                rnd.hands[i][card_ids[card_constant]] = 1

        return rnd
