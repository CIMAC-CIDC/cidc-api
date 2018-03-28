#!/usr/bin/env python3
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""


import json
import logging
import argparse
from os import environ as env
from urllib.request import urlopen

from jose import jwt
from eve import Eve
from eve.auth import TokenAuth
from eve_swagger import swagger, add_documentation
from flask import (
    current_app as app,
    jsonify,
    _request_ctx_stack
)
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv, find_dotenv

from rabbit_handler import RabbitMQHandler
import constants
import hooks

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-t', '--test', help='Run application in test mode', action='store_true')
ARGS = PARSER.parse_args()
LOGGER = logging.getLogger('ingestion-api')
LOGGER.setLevel(logging.DEBUG)
ALGORITHMS = ["RS256"]

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = 'https://' + AUTH0_DOMAIN + '/userinfo'


class BearerAuth(TokenAuth):
    """[summary]

    Arguments:
        BasicAuth {[type]} -- [description]
    """
    def check_auth(self, token, allowed_roles, resource, method):
        """[summary]

        Arguments:
            token {[type]} -- [description]
            allowed_roles {[type]} -- [description]
            resource {[type]} -- [description]
            method {[type]} -- [description]
        """
        return token_auth(token)


def add_rabbit_handler() -> None:
    """
    Adds a RabbitMQ hook the the logging object.
    """
    RABBIT = RabbitMQHandler('amqp://rabbitmq')
    LOGGER.addHandler(RABBIT)


app = Eve(
    'ingestion_api',
    auth=BearerAuth,
    settings='settings.py'
)

app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = {
    'title': 'CIDC API',
    'version': '0.1',
    'description': 'CIDC Data Upload AI',
    'termsOfService': '',
    'contact': {
        'name': 'L'
    },
    'license': {
        'name': 'MIT'
    },
    'schemes': ['http', 'https']
}

add_documentation({'paths': {'/status': {'get': {'parameters': [
    {
        'in': 'query',
        'name': 'foobar',
        'required': False,
        'description': 'special query parameter',
        'type': 'string'
    }]
}}}})

app.secret_key = constants.SECRET_KEY
app.debug = True


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@app.errorhandler(Exception)
def handle_auth_error(ex):
    print(ex)
    if ex.message:
        response = jsonify(message=ex.message)
        return response
    else:
        return jsonify(message=ex)

oauth = OAuth(app)
auth0 = oauth.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile',
        'audience': AUTH0_AUDIENCE
    },
    base_url='https://%s' % AUTH0_DOMAIN,
    access_token_method='POST',
    access_token_url='/oauth/token',
    authorize_url='/authorize',
)


def token_auth(token):
    """
    Checks if the supplied token is valid.

    Arguments:
        token {[type]} -- [description]

    Raises:
        AuthError -- [description]
        AuthError -- [description]
        AuthError -- [description]
        AuthError -- [description]

    Returns:
        [type] -- [description]
    """
    print('token_auth called')
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            print('Expired Signature Error')
            raise AuthError(
                {
                    "code": "token_expired",
                    "description": "token is expired"
                },
                401
            )
        except jwt.JWTClaimsError as claims:
            print(claims)
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer"
                },
                401
            )
        except Exception as err:
            print(err)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                },
                401
            )

        _request_ctx_stack.top.current_user = payload
        return True
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        },
        401
    )


@app.after_request
def after_request(response):
    """A function to add google path details to the response header when files are uploaded

    Decorators:

        app -- Flask decorator for application

    Arguments:
        response {dict} -- HTTP response.

    Returns:
        dict -- HTTP response with modified headers.
    """
    response.headers.add('google_url', app.config['GOOGLE_URL'])
    response.headers.add('google_folder_path', app.config['GOOGLE_FOLDER_PATH'])
    return response


@app.errorhandler(500)
def custom500(error):
    if error.description:
        print(error.description)
        return jsonify({'message': error.description}), 500
    else:
        print(error)
        return jsonify({'message': error}), 500


def create_app():
    """
    Configures the eve app.
    """

    # Ingestion Hooks
    app.on_updated_ingestion += hooks.process_data_upload
    app.on_insert_ingestion += hooks.register_upload_job

    # Data Hooks
    app.on_insert_data += hooks.serialize_objectids
    app.on_inserted_data += hooks.check_for_analysis

    # Analysis Hooks
    app.on_insert_analysis += hooks.register_analysis
    app.on_pre_GET_status += hooks.get_job_status

    # Pre get filter hook.
    app.on_pre_GET += hooks.filter_on_id

    if ARGS.test:
        app.config['TESTING'] = True
        app.config['MONGO_HOST'] = 'localhost'
    else:
        add_rabbit_handler()


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=5000)
