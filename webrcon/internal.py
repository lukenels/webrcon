
from flask import Blueprint, g, render_template, request

from .db import get_db

bp = Blueprint('internal', __name__, url_prefix='/internal')

@bp.route('/diamonds', methods=('POST',))
def diamonds():

    db = get_db()

    db.execute(
        "INSERT INTO diamonds (number, timestamp) VALUES (?, datetime('now'))",
        (request.form.get('number'),)
    )

    db.commit()

    return ""
