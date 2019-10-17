# HSLU
#
# Created by Thomas Koller on 12.10.18
#
"""
Example how to use flask to create a service for one or more players
"""
import logging

from jass.player_service.player_service_app import PlayerServiceApp
from jass.player.random_player_schieber import RandomPlayerSchieber
from jass.player.stdin_player_schieber import StdinPlayerSchieber
from jass.player.mcts.my_mcts_player import MyMCTSPlayer


def create_app():
    """
    This is the factory method for flask. It is automatically detected when flask is run, but we must tell flask
    what python file to use:

        export FLASK_APP=my_player_service.py
        export FLASK_ENV=development
        flask run --host=0.0.0.0 --port=8888
    """
    logging.basicConfig(level=logging.DEBUG)

    # create and configure the app
    app = PlayerServiceApp('my_player_service')

    # you could use a configuration file to load additional variables
    # app.config.from_pyfile('my_player_service.cfg', silent=False)

    # add some players
    app.add_player('MctsCheatingPlayer', MyMCTSPlayer)
    # app.add_player('stdin', StdinPlayerSchieber())
    app.add_player('random', RandomPlayerSchieber())

    return app
