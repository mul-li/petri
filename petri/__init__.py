import os
import os.path
import base64

from flask import Flask
from flask_qrcode import QRcode

from celery import Celery

import pkg_resources

from mulli import Mulli
from mulli import Celery as CeleryExt

config_file = os.path.abspath('config.json')

qrcode = QRcode()

celery = Celery(__name__)

celery_ext = CeleryExt()
mulli_ext = Mulli()


def create_app():

    app = Flask(__name__)

    try:
        app.config.from_json(config_file)
    except FileNotFoundError:
        pass

    qrcode.init_app(app)
    mulli_ext.init_app(app)

    _default_secret_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', _default_secret_key)

    app.config['SITE_TITLE'] = app.config.get('PETRI_SITE_TITLE', 'Petri')
    app.config['ONION_ADDRESS'] = app.config.get('PETRI_ONION_ADDRESS', None)
    app.config['DATABASE'] = app.config.get('PETRI_DATABASE', 'petri.pickle')

    app.config.setdefault('PETRI_CELERY_BROKER_URL', 'pyamqp://petri:petri@localhost:5672/petri')
    celery_config = app.config.get_namespace('PETRI_CELERY_', lowercase=False)
    celery_ext.init_app(app, celery_config)

    from .base36 import Base36Converter
    app.url_map.converters['base36'] = Base36Converter

    from .views import root_page
    app.register_blueprint(root_page)

    from .api import api_page
    app.register_blueprint(api_page, url_prefix='/api')

    @app.context_processor
    def inject_version():
        return dict(APP_VERSION=pkg_resources.require('petri')[0].version)

    @app.context_processor
    def inject_index_title():
        return dict(INDEX_TITLE='Short it!')

    return app


app = create_app()
