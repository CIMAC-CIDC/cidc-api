#!/usr/bin/env python3
"""
This file defines the basic behavior of the eve application.

Users upload files to the google bucket, and then run cromwell jobs on them
"""
import json
import logging
from urllib.request import urlopen
import requests
from jose import jwt
from eve import Eve
from eve.auth import TokenAuth
from flask import (
    current_app as APP,
    jsonify,
    _request_ctx_stack
)
from flask_oauthlib.client import OAuth
from cidc_utils.loghandler import StackdriverJsonFormatter
import hooks
from constants import (
    AUTH0_AUDIENCE,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, ALGORITHMS, AUTH0_PORTAL_AUDIENCE
)


class BearerAuth(TokenAuth):
    """
    Handles bearer token authorization.

    Arguments:
        BasicAuth {[type]} -- [description]
    """
    def check_auth(self, token, allowed_roles, resource, method):
        """[summary]

        Arguments:
            token {dict} -- JWT token.
            allowed_roles {[str]} -- Array of strings of user roles.
            resource {string} -- Endpoint being accessed.
            method {[type]} -- [description]
        """
        return token_auth(token)


APP = Eve(
    'ingestion_api',
    auth=BearerAuth,
    settings='settings.py',
)

APP.debug = False


# Format error response and append status code.
class AuthError(Exception):
    """
    [summary]

    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    [summary]

    Arguments:
        ex {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

OAUTH = OAuth(APP)
AUTH0 = OAUTH.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile email',
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
    json_url = "https://" + AUTH0_DOMAIN + "/.well-known/jwks.json"
    jsonurl = urlopen(json_url)
    jwks = json.loads(jsonurl.read())

    if not token:
        logging.warning({
            'message': 'no token received',
            'category': 'WARNING-EVE-AUTH'
        })
        return False

    unverified_header = None
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError as err:
        print(err)

    if not jwks:
        logging.warning({
            'message': 'no jwks key',
            'category': 'WARNING-EVE-AUTH'
        })
        return False

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

        # Extract audience and see if it's either the
        # ingestion APIs audience or the Portal's.
        # This enables us to validate portal's tokens.
        jwt_aud = jwt.get_unverified_claims(token)["aud"]

        audience_to_verify = AUTH0_AUDIENCE
        request_from_portal = False

        if AUTH0_PORTAL_AUDIENCE is not None and jwt_aud == AUTH0_PORTAL_AUDIENCE:
            audience_to_verify = AUTH0_PORTAL_AUDIENCE
            request_from_portal = True

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=audience_to_verify,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
        except jwt.ExpiredSignatureError:
            logging.error({
                'message': 'Expired Signature Error',
                'category': 'ERROR-EVE-AUTH'
                })
            raise AuthError(
                {
                    "code": "token_expired",
                    "description": "token is expired"
                },
                401
            )
        except jwt.JWTClaimsError as claims:
            logging.error({
                'message': 'JWT Claims error',
                'category': 'ERROR-EVE-AUTH',
            }, exc_info=True)
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer"
                },
                401
            )
        except Exception as err:
            logging.error({
                'message': 'Unspecified Auth Error',
                'category': 'ERROR-EVE-AUTH'
            }, exc_info=True)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token."
                },
                401
            )

        # Get user e-mail from userinfo endpoint.
        if request_from_portal:
            _request_ctx_stack.top.current_user = payload

            log = 'Authenticated user: ' + payload["email"]
            logging.info({
                'message': log,
                'category': 'EVE-LOGIN'
            })

            return True
        elif 'gty' not in payload:
            res = requests.get(
                'https://cidc-test.auth0.com/userinfo',
                headers={"Authorization": 'Bearer {}'.format(token)}
            )

            if not res.status_code == 200:
                logging.error({
                    'message': "There was an error fetching user information",
                    'category': 'EVE-ERROR-AUTH'
                })
                raise AuthError(
                    {
                        "code": "No_info",
                        "description": "No userinfo found at endpoint"
                    },
                    401
                )

            payload['email'] = res.json()['email']
            _request_ctx_stack.top.current_user = payload
            log = 'Authenticated user: ' + payload
            logging.info({
                'message': log,
                'category': 'EVE-LOGIN'
            })
            return True
        else:
            payload['email'] = "taskmanager-client"
            _request_ctx_stack.top.current_user = payload
            return True
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        },
        401
    )


@APP.after_request
def after_request(response):
    """
    A function to add google path details to the response header when files are uploaded

    Decorators:

        app -- Flask decorator for application

    Arguments:
        response {dict} -- HTTP response.

    Returns:
        dict -- HTTP response with modified headers.
    """
    response.headers.add('google_url', APP.config['GOOGLE_URL'])
    response.headers.add('google_folder_path', APP.config['GOOGLE_FOLDER_PATH'])
    return response


@APP.errorhandler(500)
def custom500(error):
    """
    Custom error handler to send a message with a 500 error.

    Arguments:
        error {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    try:
        logging.error({
            'message': error.description,
            'category': 'ERROR-EVE-500'
        })
        return jsonify({'message': error.description}), 500
    except AttributeError:
        err_str = str(error)
        return jsonify({'message': err_str}), 500


def create_app():
    """
    Configures the eve app.
    """
    # Configure Stackdriver logging.
    APP.logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    formatter = StackdriverJsonFormatter()
    log_handler.setFormatter(formatter)
    APP.logger.addHandler(log_handler)

    APP.logger.info({
        'message': 'LOGGER CONFIGURED',
        'category': 'EVE-TEST-LOGGING'
    })

    # Ingestion Hooks
    APP.on_updated_ingestion += hooks.process_data_upload
    APP.on_insert_ingestion += hooks.register_upload_job

    # Data Hooks
    APP.on_insert_data += hooks.serialize_objectids
    APP.on_inserted_data += hooks.check_for_analysis

    # Analysis Hooks
    APP.on_insert_analysis += hooks.register_analysis

    # Pre get filter hook.
    APP.on_pre_GET += hooks.filter_on_id


if __name__ == '__main__':
    create_app()
    APP.run(host='0.0.0.0', port=5000)

if __name__ != '__main__':
    create_app()
