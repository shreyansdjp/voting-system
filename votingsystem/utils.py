from functools import wraps
from flask import redirect, url_for

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if True:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function