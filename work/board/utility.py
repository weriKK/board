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

    handler = RotatingFileHandler(log_path, max_size, backup_count)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    return handler


def log_method_call(method):
    def wrapped(*args, **kwargs):
        args[0]._log(method.__name__+"() START")
        ret_val = method(*args, **kwargs)
        args[0]._log(method.__name__+"() END")
        return ret_val
    return wrapped
