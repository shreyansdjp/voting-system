from . import app
from flask import render_template, url_for, flash, redirect, flash
from .utils import is_admin

########### USERS ###########
@app.route('/')
def index():
    return render_template("users/verify.html")


########### SUPERADMIN ###########
@app.route('/admin')
def admin_login():
    return render_template("admin/login.html")

########### ADMIN ###########


########### PARTIES ###########
