from flask import session
from user.model import Users
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'logged_in' in session:
            return {'Error': 'You have to login first', 'Code': 409}
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'logged_in' in session:
            return {'Error': 'You have to login first', 'Code': 409}
        user_id = session['user_id']
        user = Users.objects.filter(id=user_id).first()
        if not user.is_admin:
            return {'Error': 'User must be admin', 'Code': 409}
        return f(*args, **kwargs)

    return decorated
