# HSLU
#
# Created by Ruedi Arnold on 18.01.2018
#
"""
Code for the validation and parsing of requests to a Jass player service.
"""

import json

from jass.base.player_round import PlayerRound
from jass.base.const import *

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

    def get_parsed_round(self) -> PlayerRound:
        """
        Returns the parsed round object. Attention: call only if is_valid_request() returns True.
        Returns:
            the round object created by this parser.
        """
        return self._rnd

    def get_error_message(self) -> str:
        """
            Returns the an error message, indicating why parsing failed.
            Attention: call only if is_valid_request() returns False.
            Returns:
                a (hopefully) helpful error message
        """
        return self._error_msg

    def _parse_request(self):
        """
        Abstract method to parse the request set in the init method.
        If is_valid_request returns true, the parsed data can be accessed by calling get_parsed_round().
        """
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
                self._error_msg = ERROR_MSG_PREFIX + 'no top-level element \"' + element +\
                                  '\" found in entry: {}'.format(json_obj)
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

        self._rnd = PlayerRound()
        self._rnd.dealer = self._request_dict['dealer']
        if 'tss' in self._request_dict and self._request_dict['tss'] == 1:
            self._rnd.forehand = False
            self._rnd.declared_trump = partner_player[next_player[self._rnd.dealer]]
        else:
            self._rnd.forehand = True
            self._rnd.declared_trump = next_player[self._rnd.dealer]

        found_current_hand = False
        for player_data in self._request_dict['player']:
            if 'hand' in player_data:
                hand = player_data['hand']
                if isinstance(hand, list) and len(hand) > 0:
                    if found_current_hand:
                        self._error_msg = ERROR_MSG_PREFIX + 'found second current hand \"' + player_data + '\"'
                        return
                    else:
                        found_current_hand = True
                        int_cards = convert_str_encoded_cards_to_int_encoded(hand)
                        self._rnd.hand = get_cards_encoded(int_cards)

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

        jass_typ = self._request_dict['jassTyp']
        if jass_typ not in VALID_JASS_TYPES:
            self._error_msg = ERROR_MSG_PREFIX + 'Illegal \"jassTyp\": \"' + jass_typ + \
                              '\" found in entry: {}'.format(self._request_dict)
            return

        player_round = PlayerRound()
        player_round.dealer = self._request_dict['dealer']
        player_round.trump = self._request_dict['trump']
        if 'tss' in self._request_dict and self._request_dict['tss'] == 1:
            player_round.forehand = False
            player_round.declared_trump = partner_player[next_player[player_round.dealer]]
        else:
            player_round.forehand = True
            player_round.declared_trump = next_player[player_round.dealer]

        for i, trick_dict in enumerate(self._request_dict['tricks']):
            player_round.trick_winner[i] = trick_dict['win']
            player_round.trick_first_player[i] = trick_dict['first']
            cards = trick_dict['cards']
            for j in range(len(cards)):
                player_round.tricks[i, j] = card_ids[cards[j]]
            if len(cards) == 4:
                # complete trick of 4 cards
                player_round.nr_tricks +=  1
                player_round.trick_points[i] = trick_dict['points']
                if player_round.trick_winner[i] == 0 or player_round.trick_winner[i] == 2:
                    player_round.points_team_0 += player_round.trick_points[i]
                else:
                    player_round.points_team_1 += player_round.trick_points[i]
                player_round.winner = trick_dict['win']
                player_round.trick_points[i] = trick_dict['points']

            else:
                # incomplete trick
                player_round.trick_points[i] = trick_dict['points']
                for j in range(len(cards)):
                    player_round.tricks[i, j] = card_ids[cards[j]]

        found_current_hand = False
        for player_data in self._request_dict['player']:
            if 'hand' in player_data:
                hand = player_data['hand']
                if isinstance(hand, list) and len(hand) > 0:
                    if found_current_hand:
                        self._error_msg = ERROR_MSG_PREFIX + 'found second current hand \"' + player_data + '\"'
                        return
                    else:
                        found_current_hand = True
                        int_cards = convert_str_encoded_cards_to_int_encoded(hand)
                        player_round.hand = get_cards_encoded(int_cards)

        player_round._calculate_points_from_tricks()
        self._rnd = player_round
        self._valid_request = True
