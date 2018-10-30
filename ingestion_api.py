#!/usr/bin/env python3
"""
Configures and runs the API.
"""
import datetime
import json
import logging
from typing import List
from urllib.request import urlopen
import redis

import requests
from cidc_utils.loghandler import StackdriverJsonFormatter
from eve import Eve
from eve.auth import TokenAuth
from flask import _request_ctx_stack
from flask import current_app as APP
from flask import jsonify
from flask_oauthlib.client import OAuth
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
        role = role_auth(email, allowed_roles, resource, method)
        return email and role


REDIS_INSTANCE = redis.StrictRedis(host="localhost", port=6379, db=0)
APP = Eve(
    "ingestion_api", auth=BearerAuth, settings="settings.py", redis=REDIS_INSTANCE
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

    if allowed_roles:
        lookup["role"] = {"$in": allowed_roles}

    account = accounts.find_one(lookup)

    # If account found, update last access.
    if account:
        log = "user roles for resource (%s) match scope, accepted: %s" % (
            resource,
            email,
        )
        logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
        if not resource == "accounts":
            accounts.update(
                {"_id": account["_id"]},
                {
                    "$set": {
                        "last_access": datetime.datetime.now(
                            datetime.timezone.utc
                        ).isoformat()
                    }
                },
            )

            log = "User: " + email + " last login updated"
            logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
    else:
        log = "failed permissions check for: " + email
        logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
    return account


def ensure_user_account_exists(email_address: str) -> None:
    """
    Take an email address and verify an account exists with that username.
    This is useful for novel signups that we can't check a role for yet,
    because the account doesn't exist. Default the role and applicable dates.

    :param email_address:
    :return:
    """
    db_accounts = APP.data.driver.db["accounts"]
    lookup = {"username": email_address}
    lookup_account = db_accounts.find_one(lookup)

    if not lookup_account:
        db_accounts.insert(
            {
                "username": email_address,
                "email": email_address,
                "account_create_date": datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat(),
                "role": "registrant",
                "registered": False,
            }
        )

        log = "Creating document in ACCOUNTS collection for username %s" % email_address
        logging.info({"message": log, "category": "INFO-EVE-LOGIN"})


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
        logging.warning(
            {"message": "no token received", "category": "WARNING-EVE-AUTH"}
        )
        return False

    unverified_header = None
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        logging.error(
            {"message": "Biomarker upload failed", "category": "ERROR-CELERY-AUTH"},
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
                issuer="https://" + AUTH0_DOMAIN + "/",
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
                {"message": "JWT Claims error", "category": "ERROR-EVE-AUTH"},
                exc_info=True,
            )
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer",
                },
                401,
            )
        except Exception:
            logging.error(
                {"message": "Unspecified Auth Error", "category": "ERROR-EVE-AUTH"},
                exc_info=True,
            )
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                401,
            )

        # Get user email from userinfo endpoint.
        if request_from_portal:
            _request_ctx_stack.top.current_user = payload

            ensure_user_account_exists(payload["email"])

            log = "Authenticated user: " + payload["email"]
            logging.info({"message": log, "category": "EVE-LOGIN"})

            return payload["email"]
        elif "gty" not in payload:
            res = requests.get(
                "https://" + AUTH0_DOMAIN + "/userinfo",
                headers={"Authorization": "Bearer {}".format(token)},
            )

            if not res.status_code == 200:
                logging.error(
                    {
                        "message": "There was an error fetching user information",
                        "category": "ERROR-EVE-AUTH",
                    }
                )
                raise AuthError(
                    {"code": "No_info", "description": "No userinfo found at endpoint"},
                    401,
                )

            payload["email"] = res.json()["email"]
            _request_ctx_stack.top.current_user = payload
            log = "Authenticated user: " + payload["email"]
            logging.info({"message": log, "category": "FAIR-EVE-LOGIN"})
            return payload["email"]
        else:
            payload["email"] = "celery-taskmanager"
            _request_ctx_stack.top.current_user = payload
            return payload["email"]
    raise AuthError(
        {"code": "invalid_header", "description": "Unable to find appropriate key"}, 401
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
    response.headers.add("google_url", APP.config["GOOGLE_URL"])
    response.headers.add("google_folder_path", APP.config["GOOGLE_FOLDER_PATH"])
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
        errorlog = str(error)
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
        err_str = str(error)
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
    APP.on_accounts_inserted += hooks.log_user_create
    APP.on_accounts_updated += hooks.log_user_modified

    # Ingestion Hooks
    APP.on_updated_ingestion += hooks.process_data_upload
    APP.on_insert_ingestion += hooks.register_upload_job

    # Data Hooks
    APP.on_insert_data += hooks.serialize_objectids
    APP.on_inserted_data += hooks.check_for_analysis
    APP.on_updated_data += hooks.data_patched
    APP.on_inserted_data_edit += hooks.check_for_analysis
    APP.on_insert_data_edit += hooks.serialize_objectids

    # Analysis Hooks
    APP.on_insert_analysis += hooks.register_analysis

    # Pre get filter hook.
    APP.on_pre_GET += hooks.filter_on_id

    # Logging request related hooks
    APP.on_post_PATCH += hooks.log_patch_request
    APP.on_post_POST += hooks.log_post_request
    APP.on_post_DELETE += hooks.log_delete_request


if __name__ == "__main__":
    configure_logging()
    add_hooks()
    APP.run(host="0.0.0.0", port=5000)

if __name__ != "__main__":
    configure_logging()
    add_hooks()
