
from flask import g, current_app

import mcrcon

def get_rcon():
    if 'rcon' not in g:
        g.rcon = mcrcon.MCRcon()
        g.rcon.connect(
            current_app.config.get('RCON_HOST'),
            current_app.config.get('RCON_PORT'),
            current_app.config.get('RCON_PASSWORD'),
        )
    return g.rcon
