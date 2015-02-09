from .extensions import basicAuth
from flask import make_response, jsonify


# Authorization: Basic c2F2OnB5dGhvbg==
@basicAuth.get_password
def get_password(username):
    if 'sav' == username:
        return 'python'
    return None


@basicAuth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)
