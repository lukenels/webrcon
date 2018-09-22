
from .db import get_db

def exists_user_with_username(mc_username):
    return get_db().execute('SELECT * FROM user WHERE mc_username = ?', (mc_username,)).fetchone() is not None

