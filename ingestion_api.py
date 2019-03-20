#!/usr/bin/env python3
"""
Configures and runs the API.
"""
import json
import logging
from typing import List, Tuple
from urllib.request import urlopen
import redis

import requests
from cidc_utils.loghandler import StackdriverJsonFormatter
from eve import Eve
from eve.auth import TokenAuth
from eve_swagger import swagger
from flask import _request_ctx_stack
from flask import jsonify
from authlib.flask.client import OAuth
from jose import jwt

import hooks
from settings import (
    ALGORITHMS,
    AUTH0_AUDIENCE,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_DOMAIN,
    AUTH0_PORTAL_AUDIENCE,
)


class BearerAuth(TokenAuth):
    """
    Handles bearer token authorization.

    Arguments:
        BasicAuth {[type]} -- [description]
    """

    def check_auth(
        self, token: dict, allowed_roles: List[str], resource: str, method: str
    ) -> Tuple[str, str]:
        """
        Validates the user's token and ensures that they have the appropriate validation to use
        the given endpoint.

        Arguments:
            token {dict} -- JWT token.
            allowed_roles {List[str]} -- Array of strings of user roles.
            resource {str} -- Endpoint being accessed.
            method {str} -- HTTP method (GET, POST, PATCH, DELETE)
        """
        try:
            email = token_auth(token)
            role = role_auth(email, allowed_roles, resource, method)
            if resource == "accounts_create":
                return True
            if role and "role" in role:
                role_value = role["role"]
                user = _request_ctx_stack.top.current_user
                user["role"] = role_value
            return email and role
        except KeyError:
            return False


REDIS_INSTANCE = redis.StrictRedis(host="localhost", port=6379, db=0)
APP = Eve(
    "ingestion_api", auth=BearerAuth, settings="settings.py", redis=REDIS_INSTANCE
)
APP.debug = False
APP.register_blueprint(swagger)
APP.config["SWAGGER_INFO"] = {
    "title": "CIDC Ingestion API",
    "version": "1.0",
    "description": "The CIDC ingestion API",
    "termsOfService": "To be added",
    "contact": {
        "name": "support",
        "url": "https://github.com/dfci/cidc-ingestion-api/README",
    },
    "license": {
        "name": "MIT",
        "url": "https://github.com/dfci/cidc-ingestion-api/blob/master/LICENSE",
    },
    "schemes": ["http", "https"],
}


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
AUTH0 = OAUTH.register(
    "auth0",
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={"scope": "openid profile email", "audience": AUTH0_AUDIENCE},
    base_url="https://%s" % AUTH0_DOMAIN,
    access_token_method="POST",
    access_token_url="/oauth/token",
    authorize_url="/authorize",
)


def role_auth(email: str, allowed_roles: List[str], resource: str, method: str) -> dict:
    """
    Checks to make sure the person's role authorizes them to access an endpoint.

    Arguments:
        email {str} -- User's email.
        allowed_roles {List[str]} -- List of allowed roles for the resource.

    Returns:
        dict -- User's account if found.
    """
    accounts = APP.data.driver.db["accounts"]
    lookup = {"email": email}
    account = accounts.find_one(lookup)

    # If account found...
    if account:
        hooks.update_last_access(email)  # Update last login.
        # If its accounts info or create, just return true.
        if resource in {"accounts_create", "accounts_info"}:
            return lookup
        # Otherwise, they need to be registered.
        if not account["approved"]:
            return None
        # If they are registered, check permissions.
        if account["role"] in allowed_roles:
            log = "User roles for resource (%s) match scope, accepted: %s" % (
                resource,
                email,
            )
            logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
            return account

        log = "Permissions check failed for user: %s against resource %s" % (
            email,
            resource,
        )
        logging.info({"message": log, "category": "FAIR-EVE-FAILED-PERMISSIONS"})
        return None
    elif resource == "accounts_create":  # If no account, it has to be accounts_create.
        return lookup

    # Otherwise fail.
    log = "Permissions check failed for unregistered user: %s against resource %s" % (
        email,
        resource,
    )
    logging.info({"message": log, "category": "FAIR-EVE-UNREGISTERED"})
    return None


def validate_payload(token: dict, rsa_key: str, audience_to_verify: str) -> dict:
    """
    Decodes the token and checks it for validity.

    Arguments:
        token {dict} -- JWT
        rsa_key {str} -- rsa_key
        audience_to_verify {str} -- parameter to use as the audience.

    Raises:
        AuthError -- Caused by an expired signature.
        AuthError -- Caused by invalid claims.

    Returns:
        dict -- Decoded token as a dictionary.
    """
    try:
        return jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=audience_to_verify,
            issuer="https://%s/" % AUTH0_DOMAIN,
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_iat": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iss": True,
                "verify_sub": True,
                "verify_jti": True,
                "verify_at_hash": False,
                "leeway": 0,
            },
        )
    except jwt.ExpiredSignatureError:
        logging.error(
            {"message": "Expired Signature Error", "category": "ERROR-EVE-AUTH"}
        )
        raise AuthError(
            {"code": "token_expired", "description": "token is expired"}, 401
        )
    except jwt.JWTClaimsError:
        logging.error(
            {"message": "JWT Claims error", "category": "ERROR-EVE-AUTH"}, exc_info=True
        )
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "incorrect claims, please check the audience and issuer",
            },
            401,
        )


def check_user_exists(email: str) -> bool:
    """[summary]

    Arguments:
        email {str} -- [description]

    Returns:
        bool -- [description]
    """
    db_accounts = APP.data.driver.db["accounts"]
    lookup_account = db_accounts.find_one({"username": email})
    return bool(lookup_account)


def token_auth(token: dict) -> str:
    """
    Checks if the supplied token is valid.

    Arguments:
        token {dict} -- JWT token.

    Raises:
        AuthError -- [description]

    Returns:
        str -- Authorized user's email.
    """
    jwks = json.loads(urlopen("https://%s/.well-known/jwks.json" % AUTH0_DOMAIN).read())

    if not token:
        logging.warning(
            {"message": "no token received", "category": "WARNING-EVE-AUTH"}
        )
        return False

    unverified_header = None
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        logging.error(
            {
                "message": "Problem fetched unverfied header",
                "category": "ERROR-CELERY-AUTH",
            },
            exc_info=True,
        )

    if not jwks:
        logging.warning({"message": "no jwks key", "category": "WARNING-EVE-AUTH"})
        return False

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if not rsa_key:
        logging.warning({"message": "no_rsa_key", "category": "WARNING-EVE-AUTH"})
        raise AuthError({"code": "no_rsa_key", "description": "rsa_key is null"}, 401)

    # Extract audience and see if it's either the
    # ingestion APIs audience or the Portal's.
    # This enables us to validate portal's tokens.
    jwt_aud = jwt.get_unverified_claims(token)["aud"]
    request_from_portal = False
    audience_to_verify = AUTH0_AUDIENCE

    if AUTH0_PORTAL_AUDIENCE and jwt_aud == AUTH0_PORTAL_AUDIENCE:
        audience_to_verify = AUTH0_PORTAL_AUDIENCE
        request_from_portal = True

    try:
        payload = validate_payload(token, rsa_key, audience_to_verify)
    except AuthError as ate:
        log = "Authorization failed: %s" % str(ate)
        logging.error({"message": log, "category": "ERROR-EVE-AUTH"})
        return None

    if request_from_portal:
        if not check_user_exists(payload["email"]):
            log = "User not registered: %s" % payload["email"]
            logging.info({"message": log, "category": "EVE-AUTH-UNREGISTERED"})
    elif "gty" not in payload:
        res = requests.get(
            "https://%s/userinfo" % AUTH0_DOMAIN,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        if not res.status_code == 200:
            message = "There was an error fetching user information: %s" % res.reason
            logging.error({"message": message, "category": "ERROR-EVE-AUTH"})
            raise AuthError(
                {"code": "No_info", "description": "No userinfo found at endpoint"}, 401
            )
        payload["email"] = res.json()["email"]
    else:
        payload["email"] = "celery-taskmanager"

    # Get user email from userinfo endpoint.
    _request_ctx_stack.top.current_user = payload
    log = "Authenticated user: " + payload["email"]
    logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
    return payload["email"]


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
    response.headers.add("google_url", APP.config["GOOGLE_URL"])
    response.headers.add("google_folder_path", APP.config["GOOGLE_UPLOAD_BUCKET"])
    try:
        auth_header = response.headers.pop("WWW-Authenticate")
        response.headers.add("WWW-Authenticate", auth_header.replace("Basic", "xBasic"))
    except KeyError:
        pass

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
        errorlog: str = str(error)
        logging.error({"message": errorlog, "category": "ERROR-EVE-500"})
        return jsonify({"message": str(error)}), 500
    except AttributeError:
        logging.error(
            {
                "message": "Attribute error in error format",
                "category": "ERROR-EVE-ERRORHANDLER",
            },
            exc_info=True,
        )
        err_str: str = str(error)
        return jsonify({"message": err_str}), 500


def configure_logging():
    """
    Configures the loghandler to send formatted logs to stackdriver.
    """
    # Configure Stackdriver logging.
    logger = logging.getLogger()
    logger.setLevel("INFO")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(StackdriverJsonFormatter())
    logger.addHandler(log_handler)
    logging.info({"message": "LOGGER CONFIGURED", "category": "INFO-EVE-LOGGING"})


def add_hooks():
    """
    Adds the endpoint hooks to the application object.
    """

    # Accounts hooks
    APP.on_inserted_accounts += hooks.log_user_create  # pylint: disable=E1101
    APP.on_updated_accounts += hooks.log_user_modified  # pylint: disable=E1101
    APP.on_update_accounts += hooks.manage_user_updates
    APP.on_inserted_accounts_info += hooks.log_user_create  # pylint: disable=E1101
    APP.on_insert_accounts_create += hooks.register_new_user  # pylint: disable=E1101
    APP.on_deleted_item_accounts += hooks.remove_deleted_user  # pylint: disable=E1101

    # Gene symbol hooks
    APP.on_deleted_gene_symbols += hooks.drop_gene_symbol  # pylint: disable=E1101

    # Ingestion Hooks
    APP.on_updated_ingestion += hooks.process_data_upload  # pylint: disable=E1101
    APP.on_insert_ingestion += hooks.register_upload_job  # pylint: disable=E1101

    # Data Hooks
    APP.on_insert_data += hooks.serialize_objectids  # pylint: disable=E1101
    APP.on_inserted_data += hooks.check_for_analysis  # pylint: disable=E1101
    APP.on_updated_data += hooks.data_patched  # pylint: disable=E1101
    APP.on_inserted_data_edit += hooks.check_for_analysis  # pylint: disable=E1101
    APP.on_insert_data_edit += hooks.serialize_objectids  # pylint: disable=E1101
    APP.on_fetched_item_data += hooks.generate_signed_url  # pylint: disable=E1101

    # Trials hooks
    APP.on_updated_trials += hooks.updated_trial  # pylint: disable=E1101

    # Analysis Hooks

    # Pre get filter hook.
    APP.on_pre_GET += hooks.filter_on_id  # pylint: disable=E1101

    # Logging request related hooks
    APP.on_post_PATCH += hooks.log_patch_request  # pylint: disable=E1101
    APP.on_post_POST += hooks.log_post_request  # pylint: disable=E1101
    APP.on_post_DELETE += hooks.log_delete_request  # pylint: disable=E1101


if __name__ == "__main__":
    configure_logging()
    add_hooks()
    APP.run(host="0.0.0.0", port=5000)

if __name__ != "__main__":
    configure_logging()
    add_hooks()
