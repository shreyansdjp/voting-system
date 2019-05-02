from functools import wraps
from flask import redirect, url_for, session
from PIL import Image
from . import app
import secrets, os
from datetime import datetime

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('id'):
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def is_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id'):
            if session.get('role') == 'admin':
                return redirect(url_for('get_users'))
            elif session.get('role') == 'superadmin':
                return redirect(url_for('admin_dashboard'))
            elif session.get('role') == 'party':
                pass
            elif session.get('role') == 'user':
                print('fuck off')
                return redirect(url_for('user_dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin' and session.get('role') != 'superadmin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def is_super_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['role'] != 'superadmin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def save_picture(form_picture):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/user_images', picture_fn)
    output_size = (60, 60)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def current_date():
    return datetime(datetime.now().year, datetime.now().month, datetime.now().day).date()