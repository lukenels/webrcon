
from flask import Flask, url_for, render_template, g

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

    @app.route('/')
    def hello():
        from .mojang import get_user_face
        get_user_face('Keller42')
        return render_template('hello.html')

    from . import db
    db.init_app(app)

    from . import players
    app.register_blueprint(players.bp)

    from . import internal
    app.register_blueprint(internal.bp)

    return app
