# HSLU
#
# Created by Ruedi Arnold on 18.01.2018
#
"""
Code for the validation and parsing of requests to a Jass player service.
"""

import logging

from source.jass.base.const import *
from source.jass.base.player_round import PlayerRound
from source.jass.ion.player_round_serializer import PlayerRoundSerializer

ERROR_MSG_PREFIX = 'Request Parse Error: '
VALID_JASS_TYPES = ['SCHIEBER_1000', 'SCHIEBER_2500']


class BasicRequestParser:
    """
    Base class to parse and validate requests.
    """
    def __init__(self, request_dict):
        self._request_dict = request_dict
        self._valid_request = False
        self._rnd = None
        self._error_msg = 'No Error!'
        self._logger = logging.getLogger(__name__)
        # start the parsing (including validation)
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
        # some basic error handling to provide some more meaningful error messages
        if not self._request_dict:
            return
        if not self._json_has_top_level_elements(self._request_dict,
                                                 ['dealer', 'player', 'jassTyp']):
            return

        jass_typ = self._request_dict['jassTyp']
        if jass_typ not in VALID_JASS_TYPES:
            self._error_msg = ERROR_MSG_PREFIX + 'Illegal \"jassTyp\": \"' + jass_typ + \
                              '\" found in entry: {}'.format(self._request_dict)
            self._logger.error(self._error_msg)
            return

        # use (new) Serializer class to handle actual parsing
        player_round = PlayerRoundSerializer.player_round_from_dict(self._request_dict)

        # during debugging
        player_round.assert_invariants()
        self._rnd = player_round
        self._valid_request = True

