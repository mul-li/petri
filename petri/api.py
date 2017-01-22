from flask import Blueprint, redirect, request, url_for
from flask import make_response as _make_response

import mulli

from . import utils

api_page = Blueprint('api', __name__)


valid_expires = frozenset((
    1,
    7,
    30,
    365,
    -1,
))


def make_response(content, code=200):
    response = _make_response(content)
    response.status_code = code
    response.mimetype = 'text/plain'
    return response


@api_page.route('/')
def short_it():

    url_to_short = request.args.get('url')

    if url_to_short is None:
        return make_response('Bad Request: URL parameter not specified!', 400)

    valid = request.args.get('valid', -1)

    if valid not in valid_expires:
        return make_response('Bad Request: valid parameter not acceptable!', 400)

    try:
        short_id = utils.create_short_id(url_to_short)
    except ValueError:
        return make_response('Internal Server Error', 500)

    try:
        utils.save_url(short_id, url_to_short, valid)
    except RuntimeError:
        return make_response('Internal Server Error', 500)
    return make_response(url_for('root.resolve', id=short_id, _external=True))


@api_page.route('/resolve/<base36:id>')
def resolve(id):
    try:
        url = utils.load_url(id)
    except KeyError:
        return make_response('Not found!', 404)
    except ValueError:
        mulli.remove_entry.apply_async(args=[id])
        return make_response('Not found!', 404)
    except RuntimeError:
        return make_response('Internal Server Error', 500)

    do_redirect = bool(request.args.get('redirect', False))

    if do_redirect:
        return redirect(url)
    else:
        return make_response(url)
