from flask.ext.restful import Resource
import json

## LOGGING
##############################################################################


def init_log_dir(app):
    import os

    log_dir = os.path.join(app.root_path, os.pardir, "logs")

    if 'LOG_DIR' in app.config and (not app.config["LOG_DIR"] is None):
        log_dir = app.config["LOG_DIR"]

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    return log_dir


def create_rotating_file_log_handler(log_path, max_size, backup_count, log_level, formatter):
    if not (log_path and max_size and backup_count and log_level and formatter):
        return None

    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler(log_path, maxBytes=max_size, backupCount=backup_count)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def log_method_call(method):
    def wrapped(*args, **kwargs):
        args[0]._debug_log(method.__name__+"() START")
        ret_val = method(*args, **kwargs)
        args[0]._debug_log(method.__name__+"() END")
        return ret_val
    return wrapped


class Loggable():
    _logger = None

    def __init__(self, logger=None):
        self._logger = logger

    def _debug_log(self, msg):
        if self._logger is not None:
            self._logger.debug("%s: %s", self.__class__, msg)

    def _debug_log_dict(self, msg, dictionary):
        if self._logger is not None:
            self._logger.debug("%s: %s %s", self.__class__, msg, json.dumps(dictionary))

    def _error_log(self, msg):
        if self._logger is not None:
            self._logger.error("%s: %s", self.__class__, msg)


## ERROR HANDLING
##############################################################################


def get_default_error_message(status_code):
    error_messages = {
        404: 'A resource with that ID no longer exists.'
    }

    if status_code in error_messages:
        return error_messages[status_code]
    else:
        return 'Unknown error.'


def make_error(status_code, additional_info=None, message=None):

    if message is None:
        message = get_default_error_message(status_code)

    response = {
        'status': status_code,
        'additional_info': additional_info,
        'message': message
    }

    return response, status_code


## CUSTOM RESOURCE
##############################################################################

# [TODO Kova]: Refactor this shit outta here!!
class BoardResource(Resource):
    _request_handler = None
    _format_response = None

    @classmethod
    def make_api(cls, handler, formatter):
        cls._request_handler = handler
        cls._format_response = formatter
        return cls
