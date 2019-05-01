from . import app
from flask import render_template, url_for, flash, redirect, flash, request, session
from .forms import AdminLoginForm
from .utils import is_admin
from .models import Administrators

########### USERS ###########
@app.route('/')
def index():
    return render_template("users/verify.html")


########### SUPERADMIN ###########
@app.route('/admin', methods=["POST", "GET"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        admin = Administrators.query.filter_by(email=form.email.data).first()
        print(admin)
        if admin:
            pass
        else:
            flash("Cannot find user with specified email and password", "danger")
        return redirect(url_for('admin_login'))
    return render_template("admin/login.html", form=form)


########### ADMIN ###########


########### PARTIES ###########
