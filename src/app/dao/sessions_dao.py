import datetime
from . import *


def get_session_by_id(id):
    return Session.query.get(id).first()


def get_user_from_session(session):
    user = session.serialize()["user"]
    if not user:
        raise Exception("User does not exist.")
    return user


def create_session(user_id):
    session = Session(user_id=user_id)
    db.session.add(session)
    db.session.commit()
    return session

def extract_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        raise Exception('Missing authorization header')

    bearer_token = auth_header.replace('Bearer ', '').strip()
    if not bearer_token:
        raise Exception('Missing authorization header')

    return bearer_token

def verify_session(session_token):
    session = Session.query.filter(Session.session_token == session_token).first()
    if not session or datetime.datetime.now() > session.session_expiration:
        raise Exception("Invalid session token.")
    user = get_user_from_session(session)
    return user, session


def refresh_session(update_token):
    session = Session.query.filter(Session.update_token == update_token).first()
    if not session:
        raise Exception("Invalid update token.")
    session.refresh_session()
    db.session.commit()
    return session
