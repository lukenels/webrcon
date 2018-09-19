
from flask import (
    Blueprint, g, render_template, Response
)

from . import rcon
from .mojang import get_user_face

bp = Blueprint('players', __name__, url_prefix='/players')

@bp.route('/')
def list():

    online = rcon.get_online_players()

    players = [{
        'name': n,
        'online': n in online,
    } for n in rcon.get_whitelist()]

    return render_template('players.html', players=players)

@bp.route('/face/<name>')
def face(name):
    return Response(get_user_face(name), mimetype='image/png')
