from flask import Blueprint, render_template, redirect, abort

from . import utils
from . import forms
from .base36 import base36

root_page = Blueprint('root', __name__)


@root_page.route('/', methods=('GET', 'POST'))
def index():
    form = forms.UrlForm()

    if form.validate_on_submit():
        try:
            short_id = utils.create_short_id(form.url.data)
        except ValueError:
            abort(500)

        try:
            utils.save_url(short_id, form.url.data)
        except RuntimeError:
            abort(500)

        return render_template('short.html', short_id=short_id)

    return render_template('index.html', form=form)


@root_page.route('/advanced', methods=('GET', 'POST'))
def advanced():
    form = forms.ExtendedUrlForm()

    if form.validate_on_submit():
        try:
            short_id = utils.create_short_id(form.url.data)
        except ValueError:
            abort(500)

        try:
            utils.save_url(short_id, form.url.data, form.validity.data)
        except RuntimeError:
            abort(500)
        return render_template('short.html', short_id=short_id)

    return render_template('advanced.html', form=form)


@root_page.route('/<base36:id>')
def resolve(id):
    try:
        url = utils.load_url(id)
    except KeyError:
        return render_template('not_found.html', short_id=base36(id)), 404
    except ValueError:
        utils.remove_url(id)
        return render_template('not_found.html', short_id=base36(id)), 404
    except RuntimeError:
        abort(500)

    return redirect(url)


@root_page.route('/about')
def about():
    return render_template('about.html')
