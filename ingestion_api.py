#!/usr/bin/env python3
"""
Configures and runs the API.
"""
import datetime
import json
import logging
from typing import List
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
    AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, ALGORITHMS
)


class BearerAuth(TokenAuth):
    """
    Handles bearer token authorization.

    Arguments:
        BasicAuth {[type]} -- [description]
    """
    def check_auth(self, token, allowed_roles, resource, method):
        """
        Validates the user's token and ensures that they have the appropriate validation to use
        the given endpoint.

        Arguments:
            token {dict} -- JWT token.
            allowed_roles {[str]} -- Array of strings of user roles.
            resource {string} -- Endpoint being accessed.
            method {[type]} -- [description]
        """
        email = token_auth(token)
        role = role_auth(email, allowed_roles)
        return email and role


APP = Eve(
    'ingestion_api',
    auth=BearerAuth,
    settings='settings.py',
)

APP.debug = False


# Format error response and append status code.
class AuthError(Exception):
    """
    Specifies an error processing the user's token.

    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    """
    Error handler for token related errors.

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


def role_auth(email: str, allowed_roles: List[str]) -> dict:
    """
    Checks to make sure the person's role authorizes them to access an endpoint.

    Arguments:
        email {str} -- User's email.
        allowed_roles {List[str]} -- List of allowed roles for the resource.

    Returns:
        dict -- User's account if found.
    """
    accounts = APP.data.driver.db['accounts']
    lookup = {'e-mail': email}
    if allowed_roles:
        lookup['role'] = {'$in': allowed_roles}
        log = 'User: ' + email + ' last login updated'
        logging.info({
            'message': log,
            'category': 'FAIR-EVE-LOGIN'
        })
    account = accounts.find_one(lookup)

    # If account found, update last access.
    if account:
        log = 'user roles match scope, accepted: ' + email
        logging.info({
            'message': log,
            'category': 'FAIR-EVE-LOGIN'
        })
        accounts.update(
            {'_id': account['_id']},
            {'$set': {'last_login': datetime.datetime.now(datetime.timezone.utc).isoformat()}})
    else:
        log = 'failed permissions check for: ' + email
        logging.info({
            'message': log,
            'category': 'FAIR-EVE-LOGIN'
        })
    return account


def token_auth(token):
    """
    Checks if the supplied token is valid.

    Arguments:
        token {[type]} -- [description]

    Raises:
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
    except jwt.JWTError:
        logging.error({
            'message': 'Biomarker upload failed',
            'category': 'ERROR-CELERY-AUTH'
        }, exc_info=True)

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
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
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
        except jwt.JWTClaimsError:
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
        except Exception:
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
        if 'gty' not in payload:
            res = requests.get(
                'https://cidc-test.auth0.com/userinfo',
                headers={"Authorization": 'Bearer {}'.format(token)}
            )

            if not res.status_code == 200:
                logging.error({
                    'message': "There was an error fetching user information",
                    'category': 'ERROR-EVE-AUTH'
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
            log = 'Authenticated user: ' + payload['email']
            logging.info({
                'message': log,
                'category': 'FAIR-EVE-LOGIN'
            })
            return payload['email']
        else:
            payload['email'] = "taskmanager-client"
            _request_ctx_stack.top.current_user = payload
            return payload['email']
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
        logging.error({
            'message': 'Attribute error in error format',
            'category': 'ERROR-EVE-ERRORHANDLER'
        }, exc_info=True)
        err_str = str(error)
        return jsonify({'message': err_str}), 500


def configure_logging():
    """
    Configures the loghandler to send formatted logs to stackdriver.
    """
    # Configure Stackdriver logging.
    logger = logging.getLogger()
    logger.setLevel('INFO')
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(StackdriverJsonFormatter())
    logger.addHandler(log_handler)
    logging.info({
        'message': 'LOGGER CONFIGURED',
        'category': 'INFO-EVE-LOGGING'
    })


def add_hooks():
    """
    Adds the endpoint hooks to the application object.
    """
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
    configure_logging()
    add_hooks()
    APP.run(host='0.0.0.0', port=5000)

if __name__ != '__main__':
    configure_logging()
    add_hooks()
