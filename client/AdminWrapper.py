from functools import wraps

from flask import session, redirect


def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'session_token' not in session:
            return redirect('/admin/login')

        # redirect to requested url
        return func(*args, **kwargs)

    return check_token
