
class DefaultConfig(object):

    DEBUG = False
    TESTING = False
    PROFILE = False

    ## Flask-Restful
    ################
    API_URL_PREFIX = "/api/v1.0"

    ## Cross Origin Resource Sharing (CORS)
    #######################################

    # Exposes all resources matching /api/* to Cross Origin Resource Sharing
    # and allows the Content-Type header, which is required to POST JSON
    # content cross origin.
    # Setting max_age to 3600 allows clients to cache the OPTIONS requests for an hour,
    # this way there is no need to send an OPTIONS before every PUT, POST and DELETE
    CORS_ORIGINS = '*'
    CORS_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'DELETE']
    CORS_ALLOW_HEADERS = 'Content-Type'
    CORS_MAX_AGE = 3600
    CORS_RESOURCES = r"/api/*"

    ## Database Config
    ##################
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase'
    # SQLALCHEMY_DATABASE_URI = 'oracle://scott:tiger@127.0.0.1:1521/sidname'

    SQLALCHEMY_DATABASE_URI = 'mysql://board:board@localhost/board'
    SQLALCHEMY_ECHO = False

    # Logging
    #########

    # If left unset, it will look for the logs directory outside the application's root directory
    # ..\dir\application
    # ..\dir\logs
    LOG_DIR = None
    LOG_FORMAT = '%(asctime)s %(levelname)s:%(name)s: %(message)s [in %(pathname)s:%(lineno)d]'

    # Two log files, one for errors only, one for everything
    ERROR_LOG = "board_error.log"
    ALL_LOG = "board.log"
