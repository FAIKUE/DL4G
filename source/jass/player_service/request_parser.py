# HSLU
#
# Created by Ruedi Arnold on 18.01.2018
#
"""
Code for the validation and parsing of requests to a Jass player service.
"""

import json
import logging

from jass.base.player_round import PlayerRound
from jass.base.const import *
from jass.base.round_factory import get_round

ERROR_MSG_PREFIX = 'Request Parse Error: '
VALID_JASS_TYPES = ['SCHIEBER_1000', 'SCHIEBER_2500']


class BasicRequestParser:
    """
    Base class to parse and validate requests.
    """
    def __init__(self, request_dict):
        #self._request_data = request_data
        self._request_dict = request_dict
        self._valid_request = False
        self._rnd = None
        self._error_msg = 'No Error!'
        self._logger = logging.getLogger(__name__)
        # start the parsing (including validation)
        #if self._validate_request_data():
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
            self._logger.error(self._error_msg)
            return False

        try:
            self._request_dict = json.loads(self._request_data)
        except ValueError:
            self._error_msg = ERROR_MSG_PREFIX + 'could not parse request data as json'
            self._logger.error(self._error_msg)
            return False

        if not self._request_dict:
            self._error_msg = ERROR_MSG_PREFIX + 'could not parse json data'
            self._logger.error(self._error_msg)
            return False

        return True

    def _json_has_top_level_elements(self, json_obj, elements: [str]) -> bool:
        for element in elements:
            if element not in json_obj:
                self._error_msg = ERROR_MSG_PREFIX + 'no top-level element \"' + element +\
                                  '\" found in entry: {}'.format(json_obj)
                self._logger.error(self._error_msg)
                return False

        return True


class PlayerRoundParser(BasicRequestParser):
    """
    Class to parse a complete PlayerRound.
    """

    def _parse_request(self):
        if not self._json_has_top_level_elements(self._request_dict,
                                                 ['dealer', 'player', 'jassTyp']):
            return

        jass_typ = self._request_dict['jassTyp']
        if jass_typ not in VALID_JASS_TYPES:
            self._error_msg = ERROR_MSG_PREFIX + 'Illegal \"jassTyp\": \"' + jass_typ + \
                              '\" found in entry: {}'.format(self._request_dict)
            self._logger.error(self._error_msg)
            return

        player_round = PlayerRound(dealer=self._request_dict['dealer'], jass_type=jass_typ)
        # trump might be None if case of trump request
        if 'trump' in self._request_dict:
            player_round.trump = self._request_dict['trump']
        if 'tss' in self._request_dict and self._request_dict['tss'] == 1:
            player_round.forehand = False
            player_round.declared_trump = partner_player[next_player[player_round.dealer]]
        else:
            player_round.forehand = True
            player_round.declared_trump = next_player[player_round.dealer]
        for i, trick_dict in enumerate(self._request_dict['tricks']):
            player_round.trick_first_player[i] = trick_dict['first']
            cards = trick_dict['cards']

            player_round.nr_played_cards += len(cards)
            if len(cards) == 4:
                # complete trick of 4 cards
                player_round.nr_tricks += 1
                player_round.trick_points[i] = trick_dict['points']
                player_round.trick_winner[i] = trick_dict['win']
                for j in range(len(cards)):
                    player_round.tricks[i, j] = card_ids[cards[j]]
                if player_round.trick_winner[i] == 0 or player_round.trick_winner[i] == 2:
                    player_round.points_team_0 += player_round.trick_points[i]
                else:
                    player_round.points_team_1 += player_round.trick_points[i]
            elif len(cards) > 0:
                # incomplete trick
                player_round.nr_cards_in_trick = len(cards)
                # first copy the data to the trick array
                for j in range(len(cards)):
                    player_round.tricks[player_round.nr_tricks, j] = card_ids[cards[j]]
                # then make sure the current trick points to the correct position...
                player_round.current_trick = player_round.tricks[player_round.nr_tricks]

        found_current_hand = False
        for i, player_data in enumerate(self._request_dict['player']):
            if 'hand' in player_data:
                hand = player_data['hand']
                if isinstance(hand, list) and len(hand) > 0:
                    if found_current_hand:
                        self._error_msg = ERROR_MSG_PREFIX + 'found second current hand \"' + str(player_data) + '\"'
                        self._logger.error(self._error_msg)
                        return
                    else:
                        found_current_hand = True
                        int_cards = convert_str_encoded_cards_to_int_encoded(hand)
                        player_round.hand = get_cards_encoded(int_cards)
                        # the player with the hand is the current player
                        player_round.player = i

        player_round._calculate_points_from_tricks()
        # during debugging
        player_round.assert_invariants()
        self._rnd = player_round
        self._valid_request = True


class SelectTrumpParser(PlayerRoundParser):
    """
    Class to parse a select trump request. This includes validation of the request.
    """

    def __init__(self, request_data):
        super(SelectTrumpParser, self).__init__(request_data)


class PlayCardParser(PlayerRoundParser):
    """
    Class to parse a play request. This includes validation of the request.
    """

    def __init__(self, request_data):
        super(PlayCardParser, self).__init__(request_data)
