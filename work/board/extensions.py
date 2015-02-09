from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

# Cross Origin Resource Sharing
cors = CORS()

# SQLAlchemy Database Access Layer
db = SQLAlchemy()


# HTTPBasicAuth
basicAuth = HTTPBasicAuth()
