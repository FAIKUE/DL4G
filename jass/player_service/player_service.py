# HSLU
#
# Created by Ruedi Arnold on 16.01.2018
#

"""
Code for the Jass player web interface, i.e. the "web part" receiving requests and serving them accordingly.
This file handles requests like select_trump and play_card and delegates them to a one of the registered Jass players.
"""

import configparser
import logging
import re
import socket

from http import HTTPStatus

from flask import Flask, Response, request, jsonify

from jass.base.const import card_strings
from jass.player_service.request_parser import PlayCardParser, SelectTrumpParser
from jass.player.player import Player
from jass.player.random_player import RandomPlayer
from jass.player.stdin_player import StdinPlayer

config = configparser.ConfigParser()
config.read('config.ini')


################################################
#                                              #
#  TODO: Add your own Player Instances here!   #
#                                              #
################################################

_jass_players = [RandomPlayer(), StdinPlayer()]


app = Flask(__name__)

_ip_address = '10.147.97.96'
# _ip_address = '127.0.0.1'
_port = 8888

JASS_PATH_PREFIX = '/jass-service/players/'
SELECT_TRUMP_PATH_PREFIX = '/select_trump'
PLAY_CARD_PATH_PREFIX = '/play_card'


_jass_player_dict = {}  # Containing K-V-pairs of player_name and Player instances.


@app.route(JASS_PATH_PREFIX + '<string:player_name>' + PLAY_CARD_PATH_PREFIX, methods=['POST'])
def play_card(player_name: str) -> Response:
    """
    Takes a play_card request, validates its data and returns the card to play.
    Args:
        player_name: the name of the desired player
    Returns:
        the http response to answer the given request
    """
    play_card_parser = PlayCardParser(request.data)
    if play_card_parser.is_valid_request():
        player = _get_player_for_name(player_name)
        card = player.play_card(play_card_parser.get_parsed_round())
        # card is returned as string
        data = dict(card=card_strings[card])
        return _create_ok_json_response(data)
    else:
        logging.warning(play_card_parser.get_error_message())
        return _create_bad_request_response(request)


@app.route(JASS_PATH_PREFIX + '<string:player_name>' + SELECT_TRUMP_PATH_PREFIX, methods=['POST'])
def select_trump(player_name: str) -> Response:
    """
    Takes a select_trump request, validates its data and returns the card to play.
    Args:
        player_name: the name of the desired player
    Returns:
        the http response to answer the given request

    """
    select_trump_parser = SelectTrumpParser(request.data)
    if select_trump_parser.is_valid_request():
        player = _get_player_for_name(player_name)
        trump = player.select_trump(select_trump_parser.get_parsed_round())
        data = dict(trump=trump)
        return _create_ok_json_response(data)
    else:
        logging.warning(select_trump_parser.get_error_message())
        return _create_bad_request_response(request)


@app.route(JASS_PATH_PREFIX + '<string:player_name>', methods=['GET'])
def smoke_test(player_name: str) -> Response:
    """
    Provides basic information about this players.
    Args:
        player_name:  the player name as provided in the request path.

    Returns:
        basic smoke test information.
    """
    msg = " *** Jass Player Service - SMOKE TEST ***"
    if player_name in _jass_player_dict.keys():
        return _create_ok_response(msg + " got a player '%s' here :-) *** " % player_name +
                                         " use POST requests on subpaths '%s'" % SELECT_TRUMP_PATH_PREFIX +
                                         " and '%s'. ***" % PLAY_CARD_PATH_PREFIX)
    else:
        return _create_ok_response(msg + " got NO player '%s' here :-(" % player_name)


def _create_ok_json_response(data: dict) -> Response:
    """
    Creates a http ok response with the given json data as content.
    Args:
        data: data payload as dict

    Returns:
        the http ok response with the given json data

    """
    #response = Response(response=json_str, status=HTTPStatus.OK, mimetype="application/json")
    #response.headers["Content-Type"] = "application/json; charset=utf-8"
    return jsonify(data), HTTPStatus.OK


def _create_bad_request_response(bad_request: request) -> Response:
    """
    Creates a bad request http response with the requests data content
    Args:
        bad_request: the bad request

    Returns:
        a http response of with status "bad request"
    """

    data = '{"msg":"invalid request", "data" : ' + bad_request.data.decode('utf-8') + '}'
    response = Response(response=data, status=HTTPStatus.BAD_REQUEST, mimetype="application/json")
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


def _create_ok_response(txt) -> Response:
    """
    Creates a http ok response with the given text data as content.
    Args:
        txt: the text to be used as response content.

    Returns:
        the http ok response with the given text data

    """
    response = Response(response=txt, status=HTTPStatus.OK, mimetype="text/plain")
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


def _process_and_print_players():
    """
    Checks all players registered in _jass_players, sets up _jass_player_dict and prints
    the registered players.
    """
    for player in _jass_players:
        if isinstance(player, Player):
            _jass_player_dict[convert_camel_to_snake(player.__class__.__name__)] = player
        else:
            raise Exception('\'%s\' is not an instance of class Player.' % player)
    if len(_jass_players) != len(_jass_player_dict):
        raise Exception('Players must have distinct class names.')
    print(" ********************************************************")
    print(" * Depolyed %d Jass Players, accessible at:' % len(_jass_player_dict)")
    for name in _jass_player_dict.keys():
        print(" * - " + _ip_address + ":" + str(_port) + JASS_PATH_PREFIX + name)
    print(' ********************************************************')


def _get_player_for_name(name: str) -> Player:
    if name in _jass_player_dict.keys():
        return _jass_player_dict[name]
    else:
        raise Exception("Got no player with name \'%s\'." % name)


# Inspried by https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def convert_camel_to_snake(camel_case: str) -> str:
    """
    Converts a snake_case string to a CamelCase string.
    Args:
        camel_case: the string in CamelCase format.
    Returns:
        the same string in snake_case format.

    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r'\1_\2', camel_case)
    return re.sub("([a-z0-9])([A-Z])", r'\1_\2', s1).lower()


def main():
    logging.basicConfig(level=logging.DEBUG)
    _process_and_print_players()
    # Code from https://stackoverflow.com/a/1267524
    print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
    app.run(host=_ip_address, port=_port, debug=True)


if __name__ == '__main__':
    main()
