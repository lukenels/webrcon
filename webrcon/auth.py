
from flask import (
    g, Blueprint, request,
    render_template, redirect,
    url_for, flash, session,
)

import functools
import base64
import os

from . import rcon
from . import user

from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash, generate_password_hash

from wtforms import (
    Form, PasswordField, StringField,
    validators, HiddenField,
)

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])


class RegistrationForm(FlaskForm):
    mc_username = StringField('Minecraft Username', [
        validators.DataRequired(),
    ])


class ChallengeForm(FlaskForm):
    mc_username = StringField('Minecraft Username')
    challenge = StringField('Challenge Token')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
    ])
    confirm = PasswordField('Repeat Password')


@bp.route('/register', methods=('POST', 'GET'))
def register():

    from .rcon import whisper, get_online_players

    form = RegistrationForm()
    if form.validate_on_submit():

        error = None
        mc_username = form.mc_username.data

        if form.mc_username.data not in get_online_players(nocache=True):
            error = 'Player {} is not online.'.format(mc_username)

        elif user.exists_user_with_username(mc_username):
            error = 'Account already exists for {}'.format(mc_username)

        if error is None:
            challenge = base64.encodebytes(os.urandom(15)).decode('utf8')[:-1]

            print(challenge)# FIXME remove

            rcon.whisper(mc_username, 'Psst! Your challenge is {}'.format(challenge))

            db = get_db()
            db.execute(
                'INSERT INTO challenge (mc_username, challenge) VALUES (?, ?)',
                (mc_username, challenge)
            )
            db.commit()

            return redirect(url_for('auth.challenge', mc_username=mc_username))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/challenge', methods=('POST', 'GET'))
def challenge():

    mc_username = request.args.get('mc_username')

    form = ChallengeForm()
    form.mc_username.data = mc_username

    if form.validate_on_submit():

        error = None

        mc_username = form.mc_username.data
        password = form.password.data

        challenge = get_db().execute('SELECT * from challenge WHERE mc_username = ? ORDER BY id DESC LIMIT 1',
            (mc_username,)).fetchone()

        if challenge is None:
            error = 'No challenge issued for {}'.format(mc_username)
        else:
            challenge = challenge['challenge']

        if form.challenge.data != challenge:
            error = 'Challenge incorrect!'

        if user.exists_user_with_username(mc_username):
            error = 'User already exists for minecraft username {}'.format(mc_username)

        if error is None:

            password_hash = generate_password_hash(password)

            db = get_db()

            db.execute('INSERT INTO user (mc_username, password_hash) VALUES (?, ?)',
                (mc_username, password_hash))
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/challenge.html',
        form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))


@bp.route('/login', methods=('GET', 'POST'))
def login():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        db = get_db()

        error = None
        user = db.execute(
            'SELECT * FROM user WHERE mc_username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('hello'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view



@bp.route('/whoami')
@login_required
def whoami():
    return g.user['mc_username']