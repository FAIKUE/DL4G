# HSLU
#
# Created by Ruedi Arnold on 16.01.2018
#

"""
Code for the Jass player web interface, i.e. the "web part" of receiving requests and accordingly replying to them.
Receives requests like the select_trump and play_card and delegates them to a one of the registered Jass player.
"""

import configparser
import re
from http import HTTPStatus

from flask import Flask
from flask import Response
from flask import request

from jass_player_service.request_parser import PlayCardParser
from jass_players.random_player import RandomPlayer
from jass_players.stdin_player import StdinPlayer

config = configparser.ConfigParser()
config.read('config.ini')

_jass_players = [RandomPlayer(), StdinPlayer()] # TODO: Add your own Players here!
_jass_player_class_names = []

_ip_address = '127.0.0.1'
_port = 8888

JASS_PATH_PREFIX = '/jass-service/players/'
SELECT_TRUMP_PATH_PREFIX = '/select_trump'
PLAY_CARD_PATH_PREFIX = '/play_card'

app = Flask(__name__)

@app.route(JASS_PATH_PREFIX + '<string:player>' + PLAY_CARD_PATH_PREFIX, methods=['GET'])
def XXX(player: str) -> Response:
    if player in _jass_player_class_names:
        return play_card()
    else:
        return('no valid player: ' + player)


@app.route('/subpath_jassen/play_card', methods=['POST'])
def play_card() -> Response:
    """
    takes a play_card request, validates its data and returns the card to play.
    Returns:
        the http response to answer the given request

    """
    play_card_parser = PlayCardParser(request.data)
    if play_card_parser.is_valid_request():
        card = _jass_bot.play_card(play_card_parser.get_parsed_round())
        response_ok = '{"card":"' + card + '"}'
        return _create_ok_json_response(response_ok)
    else:
        print(play_card_parser.get_error_message())
        return _create_bad_request_response(request)


@app.route('/subpath_jassen/select_trump', methods=['POST'])
def select_trump() -> Response:
    """
    takes a select_trump request, validates its data and returns the card to play.
    Returns:
        the http response to answer the given request

    """
    select_trump_parser = request_parser.SelectTrumpParser(request.data)
    if select_trump_parser.is_valid_request():
        trump = str(_jass_bot.select_trump(select_trump_parser.get_parsed_round()))
        response_ok = '{"trump":"' + trump + '"}'
        return _create_ok_json_response(response_ok)
    else:
        print(select_trump_parser.get_error_message())
        return _create_bad_request_response(request)

def _create_ok_json_response(json_str) -> Response:
    """
    creates a http ok response with the given json data as content.
    Args:
        json_str: the json string to be used as response content.

    Returns:
        the http ok response with the given json data

    """
    # ToDo: check is headers, mime type and so on are set desired
    response = Response(response=json_str, status=HTTPStatus.OK, mimetype="application/json")
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

def _create_bad_request_response(bad_request: request) -> Response:
    """
    creates a bad request http response with the requests data content
    Args:
        bad_request: the bad request

    Returns:
        a http ok response of with status "bad request"
    """

    data = '{"msg":"invalid request", "data" : ' + bad_request.data.decode('utf-8') + '}'
    response = Response(response=data, status=HTTPStatus.BAD_REQUEST, mimetype="application/json")
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

def _convert_camel_to_snake(tha_string: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', tha_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
    for player in _jass_players:
        _jass_player_class_names.append(_convert_camel_to_snake(player.__class__.__name__))
    print('********************************************************')
    print('* Depolying the following Jass Players: %s' % _jass_player_class_names)
    if len(_jass_players) > 0:
        print('* i.e. access your Player e.g. at ' + _ip_address + ':' + str(_port) + JASS_PATH_PREFIX +
              _jass_player_class_names[0] + PLAY_CARD_PATH_PREFIX)
    print('********************************************************')
    app.run(host=_ip_address, port=_port)


if __name__ == '__main__':
    main()
