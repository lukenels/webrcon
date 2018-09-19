
from werkzeug.contrib.cache import SimpleCache, RedisCache

from flask import current_app, g

from functools import wraps

def get_cache():
    if 'cache' not in g:
        if 'REDIS_HOST' in current_app.config:
            g.cache = RedisCache(current_app.config.get('REDIS_HOST'))
        else:
            g.cache = SimpleCache()
    return g.cache


def cached(key, timeout=300):
    def wrap(f):
        @wraps(f)
        def inner(*args, **kwargs):
            rkey = key.format(*args, **kwargs)
            obj = get_cache().get(rkey)
            if obj is None:
                obj = f(*args, **kwargs)
                get_cache().set(rkey, obj, timeout=timeout)
            return obj
        return inner
    return wrap
