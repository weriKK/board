from flask import Flask
# TODO(kova): try except ImportError handling?!

# Import the Task blueprint
from .todo.views import todo_blueprint

# TODO(kova) move the extension initialization into an importable module
from .extensions import cors


def create_app(config=None):
    app = Flask("board")

    init_config(app, config)
    init_database(app)
    init_extensions(app)
    init_blueprints(app)
    init_logging(app)

    return app


def init_config(app, config):
    # Load the default configuration
    app.config.from_object('board.configs.default.DefaultConfig')

    # Update the default configuration with the desired config
    app.config.from_object(config)


def init_database(app):
    from .database.db_manager import db_manager

    app.dbm = db_manager()
    app.dbm.setup_db('board', 'localhost', 3306, 'board', 'board')


def init_blueprints(app):
    app.register_blueprint(todo_blueprint, url_prefix=app.config["API_URL_PREFIX"])


def init_extensions(app):
    # Exposes the configured resources to Cross Origin Resource Sharing
    cors.init_app(app)


def init_logging(app):
    import os
    from logging import getLogger, Formatter, DEBUG, ERROR
    from board.utility import init_log_dir, create_rotating_file_log_handler

    formatter = Formatter(app.config['LOG_FORMAT'])
    log_dir = init_log_dir(app)

    all_log_path = os.path.join(log_dir, app.config['ALL_LOG'])
    all_log_file_handler = create_rotating_file_log_handler(all_log_path, 1024*1024*1, 10, DEBUG, formatter)

    error_log_path = os.path.join(log_dir, app.config['ERROR_LOG'])
    error_log_file_handler = create_rotating_file_log_handler(error_log_path, 1024*1024*1, 10, ERROR, formatter)

    # Iterate over all the loggers we need, and attach our log handlers to them
    loggers = [app.logger, getLogger('todo_logger'), getLogger('db_manager')]

    for logger in loggers:
        logger.addHandler(all_log_file_handler)
        logger.addHandler(error_log_file_handler)

        if logger is app.logger:
            logger.info('---------------------')
            logger.info('---- APP STARTED ----')
            logger.info('---------------------')

        logger.info('Logger initialized')
