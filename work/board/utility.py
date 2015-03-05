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

    def _error_log(self, msg):
        if self._logger is not None:
            self._logger.error("%s: %s", self.__class__, msg)
