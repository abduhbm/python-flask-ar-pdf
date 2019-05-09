import logging
import settings

from flask import Flask, Blueprint
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from api.restplus import utils
from api.endpoints.pdf import ns as pdf_namespace


# initialize the app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)


log = logging.getLogger(__name__)


def configue_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = settings.SEND_FILE_MAX_AGE_DEFAULT
    flask_app.debug = settings.FLASK_DEBUG


def initialize_app(flask_app):
    configue_app(flask_app)

    # prepare blueprints
    blueprint_api = Blueprint('api', __name__, url_prefix='/api')
    utils.init_app(blueprint_api)
    utils.add_namespace(pdf_namespace)
    flask_app.register_blueprint(blueprint_api)


initialize_app(app)

if __name__ == '__main__':
    app.run()

