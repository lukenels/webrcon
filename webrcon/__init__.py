
from flask import Flask, url_for, render_template, g

import os

from . import rcon

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('hello.html')

    @app.route('/players')
    def players():

        online = rcon.get_online_players()

        players = [{
            'name': n,
            'online': n in online,
        } for n in rcon.get_whitelist()]

        return render_template('players.html', players=players)

    return app
