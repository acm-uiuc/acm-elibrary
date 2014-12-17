from flask import request, redirect, url_for
from flask import current_app as app
from functools import wraps
import requests

def auth_server_post(endpoint, data):
    url = app.config['AUTH_SERVER_URL'].format(endpoint=endpoint)
    auth = (app.config['AUTH_SERVER_APP_NAME'], app.config['AUTH_SERVER_APP_PASSWORD'])
    return requests.post(url, data=data, headers=app.config['AUTH_SERVER_HEADERS'], auth=auth)

def login_required(f):
    """Checks whether user is logged in or redirects to the login page."""
    @wraps(f)
    def decorator(*args, **kwargs):
        if not valid_token():
            return redirect(url_for('views.login', **{"continue":request.url}))
        return f(*args, **kwargs)
    return decorator

def valid_token():
    valid = False
    token = request.cookies.get(app.config['COOKIE_NAME'])
    if token:
        valid = valid_session(token)
    return valid

# POST /session
#   {"username": "my_username", "password": "my_password"}
def valid_login(netid, password):
    data = app.config['AUTH_SERVER_LOGIN_DATA'].format(username=netid, password=password)
    r = auth_server_post(app.config['AUTH_SERVER_LOGIN_ENDPOINT'], data)

    if r.status_code not in [201, 400, 403]:
        request.login_error_message = "There was an error communicating with the authentication server."
        return False

    body = r.json()

    if r.status_code != 201:
        request.login_error_message = "The netid or password you entered is incorrect."
        return False

    session = {
        "token": body["token"],
        "user": {
            "name": body["user"]["name"]
        },
        "created-date": body["created-date"],
        "expiry-date": body["expiry-date"]
    }
    save_session_info(session)
    return True

def log_the_user_in(response):
    response.set_cookie(app.config['COOKIE_NAME'], request.app_session["token"], expires=request.app_session["expiry-date"])

def log_the_user_out(response):
    response.set_cookie(app.config['COOKIE_NAME'], "", expires=0)

# POST /session/{token}
def valid_session(token):
    r = auth_server_post(app.config['AUTH_SERVER_SESSION_ENDPOINT'].format(token=token), app.config['AUTH_SERVER_SESSION_DATA'])

    if r.status_code != 200:
        return False

    body = r.json()

    session = {
        "token": body["token"],
        "user": {
            "name": body["user"]["name"]
        },
        "created-date": body["created-date"],
        "expiry-date": body["expiry-date"]
    }
    save_session_info(session)
    return True

def save_session_info(session):
    request.app_session = session
