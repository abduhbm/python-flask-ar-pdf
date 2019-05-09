import logging
import settings
from flask_restplus import Api

log = logging.getLogger(__name__)

utils = Api(version='1.0', title='PDF Generator', description='export Arabic PDF')


@utils.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred'
    if settings.FLASK_DEBUG:
        log.exception(e)
    return {'message': message.strip()}, 500


@utils.errorhandler(ValueError)
def handle_value_error(e):
    if settings.FLASK_DEBUG:
        log.exception(e)
    return {'message': str(e).strip()}, 400
