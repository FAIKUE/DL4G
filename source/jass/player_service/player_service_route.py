# HSLU
#
# Created by Ruedi Arnold on 16.01.2018
# Changed to use blueprint, Thomas Koller on 12.10.2018
#

"""
Code for the Jass player web interface, i.e. the "web part" receiving requests and serving them accordingly.
This file handles requests like select_trump and play_card and delegates them to a one of the registered Jass players.
"""

import logging
from http import HTTPStatus

from flask import request, jsonify, Blueprint, current_app

from jass.base.const import card_strings
from jass.player_service.request_parser import PlayerRoundParser


JASS_PATH_PREFIX = '/jass-service/players/'
SELECT_TRUMP_PATH_PREFIX = '/select_trump'
PLAY_CARD_PATH_PREFIX = '/play_card'
SEND_INFO_PREFIX = '/game_info'

players = Blueprint(JASS_PATH_PREFIX, __name__)


@players.route('/<string:player_name>' + PLAY_CARD_PATH_PREFIX, methods=['POST'])
def play_card(player_name: str):
    """
    Takes a play_card request, validates its data and returns the card to play.
    Args:
        player_name: the name of the desired player
    Returns:
        the http response to answer the given request
    """
    if not request.is_json:
        return jsonify(error='json data expected'), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    request_dict = request.get_json()
    parser = PlayerRoundParser(request_dict)
    if parser.is_valid_request():
        player = current_app.get_player_for_name(player_name)
        if player is None:
            return jsonify(error='player not found'), HTTPStatus.BAD_REQUEST
        try:
            card = player.play_card(parser.get_parsed_round())
            # card is returned as string
            data = dict(card=card_strings[card])
            return jsonify(data), HTTPStatus.OK
        except Exception as e:
            return jsonify(error=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        logging.warning(parser.get_error_message())
        return jsonify(parser.get_error_message()), HTTPStatus.BAD_REQUEST


@players.route('/<string:player_name>' + SELECT_TRUMP_PATH_PREFIX, methods=['POST'])
def select_trump(player_name: str):
    """
    Takes a select_trump request, validates its data and returns the card to play.
    Args:
        player_name: the name of the desired player
    Returns:
        the http response to answer the given request

    """
    if not request.is_json:
        return jsonify(error='json data expected'), HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    request_dict = request.get_json()
    parser = PlayerRoundParser(request_dict)
    if parser.is_valid_request():
        player = current_app.get_player_for_name(player_name)
        trump = player.select_trump(parser.get_parsed_round())
        data = dict(trump=trump)
        return jsonify(data), HTTPStatus.OK
    else:
        logging.warning(parser.get_error_message())
        return jsonify(parser.get_error_message()), HTTPStatus.BAD_REQUEST


@players.route('/<string:player_name>', methods=['GET'])
def smoke_test(player_name: str):
    """
    Provides basic information about this players.
    Args:
        player_name:  the player name as provided in the request path.

    Returns:
        basic smoke test information.
    """
    player = current_app.get_player_for_name(player_name)
    if player is not None:
        return jsonify('Player {} here'.format(player_name)), HTTPStatus.OK
    else:
        return jsonify('No such player {}'.format(player_name)), HTTPStatus.NOT_FOUND
