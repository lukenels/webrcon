
from flask import Blueprint, g, render_template, request

bp = Blueprint('internal', __name__, url_prefix='/internal')

@bp.route('/diamonds', methods=('POST',))
def diamonds():
    print(request.form['number'])

    return None
