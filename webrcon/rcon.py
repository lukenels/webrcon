
from flask import g, current_app

import mcrcon

from .caching import get_cache, cached

def get_rcon():
    if 'rcon' not in g:
        g.rcon = mcrcon.MCRcon()
        g.rcon.connect(
            current_app.config.get('RCON_HOST'),
            current_app.config.get('RCON_PORT'),
            current_app.config.get('RCON_PASSWORD'),
        )
    return g.rcon


def get_online_players():
    return set(get_rcon().command('list').split(':')[1].split(', '))


@cached(key='player-whitelist')
def get_whitelist():

    whitelist = get_rcon().command('whitelist list').split(':')[1].split(', ')
    # Stupid minecraft returns an "and" in the list
    if len(whitelist) > 0 and ' and ' in whitelist[-1]:
        (name1, name2) = whitelist[-1].split(' and ')
        whitelist[-1] = name1
        whitelist.append(name2)

    return whitelist


def kick(player, reason=''):
    r = get_rcon().command('kick {} {}'.format(player, reason))
    return r.startswith('Kicked')
