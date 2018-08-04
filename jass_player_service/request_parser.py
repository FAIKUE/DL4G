# HSLU
#
# Created by Ruedi Arnold on 18.01.2018
#
"""
Code for the validation of requests to a jass_player_service.
"""

import json

from jass_base.game import *
from jass_base.game_const import *

ERROR_MSG_PREFIX = 'Request Parse Error: '
VALID_JASS_TYPES = ['SCHIEBER_1000', 'SCHIEBER_2500']


class BasicRequestParser:
    """
    Base class to parse and validate requests.
    """

    def __init__(self, request_data):
        self._request_data = request_data
        self._request_dict = None
        self._valid_request = False
        self._rnd = None
        self._error_msg = 'No Error!'
        # start the parsing (including validation)
        if self._validate_request_data():
            self._parse_request()

    def is_valid_request(self) -> bool:
        return self._valid_request

    def get_parsed_round(self) -> Round:
        """
        Returns the parsed round object. Attention: call only if is_valid_request() returns True.
        Returns:
            the parsed round object
        """
        return self._rnd

    def get_error_message(self) -> str:
        """
            Returns the an error message, indicating why parsing failed.
            Attention: call only if is_valid_request() returns False.
            Returns:
                the parsed round object
        """
        return self._error_msg

    def _parse_request(self):
        raise NotImplementedError('BasicRequestParser._parse_request')

    def _validate_request_data(self) -> bool:
        if not self._request_data:
            self._error_msg = ERROR_MSG_PREFIX + 'got no request data'
            return False

        try:
            self._request_dict = json.loads(self._request_data)
        except ValueError:
            self._error_msg = ERROR_MSG_PREFIX + 'could not parse request data as json'
            return False

        if not self._request_dict:
            self._error_msg = ERROR_MSG_PREFIX + 'could not parse json data'
            return False

        return True

    def _json_has_top_level_elements(self, json_obj, elements: [str]) -> bool:
        for element in elements:
            if element not in json_obj:
                self._error_msg = ERROR_MSG_PREFIX + 'no top-level element \"' + element + '\" found in entry: {}'.format(
                    json_obj)
                return False

        return True


class SelectTrumpParser(BasicRequestParser):
    """
    Class to parse a select trump request. This includes validation of the request.
    """

    def __init__(self, request_data):
        super(SelectTrumpParser, self).__init__(request_data)

    def _parse_request(self):
        if not self._json_has_top_level_elements(self._request_dict, ['dealer', 'tricks', 'player', 'jassTyp']):
            return

        if self._request_dict['jassTyp'] not in VALID_JASS_TYPES:
            self._error_msg = ERROR_MSG_PREFIX + 'Illegal \"jassTyp\": \"' + self._request_dict['jassTyp'] + \
                              '\" found in entry: {}'.format(self._request_dict)
            return

        self._rnd = Round()
        self._rnd.dealer = self._request_dict['dealer']
        if 'tss' in self._request_dict and self._request_dict['tss'] == 1:
            self._rnd.forehand = False
            self._rnd.declared_trump = partner_player[next_player[self._rnd.dealer]]
        else:
            self._rnd.forehand = True
            self._rnd.declared_trump = next_player[self._rnd.dealer]

        for player_data in self._request_dict['player']:
            found_current_hand = False
            if 'hand' in player_data:
                hand = player_data['hand']
                if isinstance(hand, list) and len(hand) > 0:
                    if found_current_hand:
                        self._error_msg = ERROR_MSG_PREFIX + 'found second current hand \"' + player_data + '\"'
                        return
                    else:
                        found_current_hand = True
                        int_cards = convert_str_encoded_cards_to_int_encoded(hand)
                        self._rnd.current_hand = get_cards_encoded(int_cards)

        self._rnd.calc_hands()
        self._valid_request = True


class PlayCardParser(BasicRequestParser):
    """
    Class to parse a play request. This includes validation of the request.
    """

    def __init__(self, request_data):
        super(PlayCardParser, self).__init__(request_data)

    def _parse_request(self):
        if not self._json_has_top_level_elements(self._request_dict,
                                                 ['dealer', 'trump', 'tricks', 'player', 'player', 'jassTyp']):
            return

        jassTyp = self._request_dict['jassTyp']
        if self._request_dict['jassTyp'] not in VALID_JASS_TYPES:
            self._error_msg = ERROR_MSG_PREFIX + 'Illegal \"jassTyp\": \"' + self._request_dict['jassTyp'] + \
                              '\" found in entry: {}'.format(self._request_dict)
            return

        self._rnd = Round()
        self._rnd.dealer = self._request_dict['dealer']
        self._rnd.trump = self._request_dict['trump']
        if 'tss' in self._request_dict and self._request_dict['tss'] == 1:
            self._rnd.forehand = False
            self._rnd.declared_trump = partner_player[next_player[self._rnd.dealer]]
        else:
            self._rnd.forehand = True
            self._rnd.declared_trump = next_player[self._rnd.dealer]

        self._rnd.current_trick = Trick()
        for i, trick_dict in enumerate(self._request_dict['tricks']):
            trick = Trick()
            trick.winner = trick_dict['win']
            trick.first_player = trick_dict['first']
            cards = trick_dict['cards']

            if len(cards) == 4:
                # it' a complete trick
                trick.cards = [card_ids[cards[0]],
                     card_ids[cards[1]],
                     card_ids[cards[2]],
                     card_ids[cards[3]]]
                trick.is_last = (i == 8)
                trick.calc_points(self._rnd.trump)
                assert (trick.points == trick_dict['points'])
                self._rnd.add_trick(trick)
            else:
                # incomplete trick
                trick.points = trick_dict['points']
                c = []
                for card in cards:
                    c.append(card_ids[card])
                trick.cards = c
                self._rnd.current_trick = trick

        for player_data in self._request_dict['player']:
            found_current_hand = False
            if 'hand' in player_data:
                hand = player_data['hand']
                if isinstance(hand, list) and len(hand) > 0:
                    if found_current_hand:
                        self._error_msg = ERROR_MSG_PREFIX + 'found second current hand \"' + player_data + '\"'
                        return
                    else:
                        found_current_hand = True
                        int_cards = convert_str_encoded_cards_to_int_encoded(hand)
                        self._rnd.current_hand = get_cards_encoded(int_cards)

        self._rnd.calc_hands()
        self._valid_request = True
