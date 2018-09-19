
from flask import (
    Blueprint, g, render_template
)

from . import rcon

bp = Blueprint('players', __name__, url_prefix='/players')

@bp.route('/')
def list():

    online = rcon.get_online_players()

    players = [{
        'name': n,
        'online': n in online,
    } for n in rcon.get_whitelist()]

    return render_template('players.html', players=players)
