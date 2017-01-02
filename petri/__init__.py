import os
import os.path
import base64

from flask import Flask
from flask_qrcode import QRcode

from celery import Celery

import pkg_resources

config_file = os.path.abspath('config.json')

qrcode = QRcode()

celery = Celery(__name__)


def create_app():

    app = Flask(__name__)

    try:
        app.config.from_json(config_file)
    except FileNotFoundError:
        pass

    qrcode.init_app(app)

    _default_secret_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', _default_secret_key)
    app.config.setdefault('PETRI_SITE_TITLE', 'Petri')
    app.config.setdefault('DATABASE', 'petri.pickle')
    app.config.setdefault('PETRI_CELERY_BROKER_URL', 'pyamqp://localhost:5672/petri')

    celery_config = app.config.get_namespace('PETRI_CELERY_')
    celery.conf.update(celery_config)

    from .base36 import Base36Converter
    app.url_map.converters['base36'] = Base36Converter

    from .views import root_page
    app.register_blueprint(root_page)

    from .api import api_page
    app.register_blueprint(api_page, url_prefix='/api')

    @app.context_processor
    def inject_version():
        return dict(PETRI_VERSION=pkg_resources.require('petri')[0].version)

    return app


app = create_app()
