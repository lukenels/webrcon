
from flask import (
    Blueprint, g, render_template, Response, redirect, url_for,
)


from flask_wtf import FlaskForm

from . import rcon
from .mojang import get_user_face
from .auth import login_required

from .caching import get_cache

bp = Blueprint('players', __name__, url_prefix='/players')

@bp.route('/')
@login_required
def list():

    online = rcon.get_online_players()

    players = [{
        'name': n,
        'online': n in online,
        'form': KickForm(),
    } for n in rcon.get_whitelist()]

    players.sort(key=lambda x : not x['online'])

    return render_template('players.html', players=players)


class KickForm(FlaskForm):
    pass


@bp.route('/kick/<name>', methods=('POST',))
@login_required
def kick(name):
    rcon.kick(name, 'Kicked from the web console')
    get_cache().delete('online-players')
    return redirect(url_for('players.list'))


@bp.route('/face/<name>')
def face(name):
    return Response(get_user_face(name), mimetype='image/png')
