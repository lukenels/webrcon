
import requests

from urllib.parse import quote
import base64
import json
import io

from PIL import Image

from .caching import cached

from flask import abort

@cached(key='minecraft-uuid-{}')
def get_uuid(username):
    url = 'https://api.mojang.com/users/profiles/minecraft/{}'.format(quote(username))
    return requests.get(url).json()['id']


@cached(key='minecraft-skin-url-{}')
def get_skin_url(uuid):
    url = 'https://sessionserver.mojang.com/session/minecraft/profile/{}'.format(quote(uuid))
    properties = requests.get(url).json()['properties']

    for prop in properties:
        if prop['name'] == 'textures':
            textures = prop['value']
            break
    else:
        abort(404)

    textures = json.loads(base64.decodebytes(textures.encode('utf8')).decode('utf8'))

    return textures['textures']['SKIN']['url']


@cached(key='minecraft-user-face-{}', timeout=60*60*2)
def get_user_face(username):
    try:
        skinurl = get_skin_url(get_uuid(username))
    except:
        abort(404)
    b = requests.get(skinurl).content
    image = Image.open(io.BytesIO(b))
    image = image.crop((8, 8, 16, 16)) # location of face
    out = io.BytesIO()
    image.save(out, format='PNG')
    return out.getvalue()
