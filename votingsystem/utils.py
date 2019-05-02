from functools import wraps
from flask import redirect, url_for
from PIL import Image
from . import app
import secrets, os

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if True:
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