from flask import Flask

# TODO(kova): try except ImportError handling?!

# Import the Task blueprint
from .todo.views import todo_blueprint

# TODO(kova) move the extension initialization into an importable module
from .extensions import cors


def create_app(config=None):
    app = Flask("board")

    init_config(app, config)
    init_logging(app)
    init_database(app)
    init_extensions(app)
    init_blueprints(app)

    return app


def init_config(app, config):
    # Load the default configuration
    app.config.from_object('board.configs.default.DefaultConfig')

    # Update the default configuration with the desired config
    app.config.from_object(config)


def init_database(app):
    from .database.db_manager import DbManager

    app.dbm = DbManager(app.logger)
    app.dbm.setup_db('board', 'localhost', 3306, 'board', 'board')


def init_blueprints(app):
    app.register_blueprint(todo_blueprint, url_prefix=app.config["API_URL_PREFIX"])


def init_extensions(app):
    # Exposes the configured resources to Cross Origin Resource Sharing
    cors.init_app(app)


def init_logging(app):
    import os
    import json
    from flask import request
    from logging import Formatter, DEBUG, INFO
    from board.utility import init_log_dir, create_rotating_file_log_handler

    formatter = Formatter(app.config['LOG_FORMAT'])
    log_dir = init_log_dir(app)

    if app.debug:

        debug_log_path = os.path.join(log_dir, app.config['DEBUG_LOG'])
        debug_log_file_handler = create_rotating_file_log_handler(debug_log_path, 1024*1024*1, 10, DEBUG, formatter)

        app.logger.addHandler(debug_log_file_handler)

    main_log_path = os.path.join(log_dir, app.config['MAIN_LOG'])
    main_log_file_handler = create_rotating_file_log_handler(main_log_path, 1024*1024*1, 10, INFO, formatter)

    # By default, the request logs are cought by Flask, because these are handled by the underlying
    # WSGI module, Werkzeug (if using the built in flask development werkzeug server).
    # access_log_path = os.path.join(log_dir, app.config['ACCESS_LOG'])
    # werkzeug_handler = create_rotating_file_log_handler(access_log_path, 1024*1024*1, 10, INFO, formatter)
    # werkzeug_logger = getLogger('werkzeug')
    # werkzeug_logger.addHandler(werkzeug_handler)

    @app.before_request
    def pre_request_logging():
        msg = "--> %s - %s %s %s" % ( request.remote_addr, request.method, request.path, request.data )

        if app.debug:
            msg += " {%s " % ( ', '.join([': '.join(x) for x in request.headers]) )

        app.logger.info(msg)

    @app.after_request
    def post_request_logging(response):
        msg = "<-- %s %s" % ( response.status, json.loads(response.get_data()) )

        if app.debug:
            msg += " {%s}" % ( ', '.join([': '.join(x) for x in response.headers]) )

        app.logger.info(msg)

        return response

    app.logger.addHandler(main_log_file_handler)
    app.logger.info('---------------------')
    app.logger.info('---- APP STARTED ----')
    app.logger.info('---------------------')
    app.logger.info('Logger initialized')
