
from flask import Flask, url_for, render_template, g

import mcrcon
import os

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

    def get_rcon():
        if 'rcon' not in g:
            g.rcon = mcrcon.MCRcon()
            g.rcon.connect(
                app.config.get('RCON_HOST'),
                app.config.get('RCON_PORT'),
                app.config.get('RCON_PASSWORD'),
            )
        return g.rcon

    @app.route('/')
    def hello():
        return render_template('hello.html')

    @app.route('/players')
    def players():
        rcon = get_rcon()
        response = rcon.command('list')
        return render_template('players.html', response=response)

    return app
