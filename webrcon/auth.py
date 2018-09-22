
from flask import (
    g, Blueprint, request,
    render_template, redirect,
    url_for, flash, session,
)

import functools

from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash, generate_password_hash

from wtforms import (
    Form, PasswordField, StringField,
    validators,
)

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])


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
            'SELECT * FROM user WHERE username = ?',
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
    return g.user['username']