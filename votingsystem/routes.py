from . import app, db
from flask import render_template, url_for, flash, redirect, flash, request, session
from .forms import AdminLoginForm, CreateElectionForm, CreateAdminForm, CreatePartyForm, CreateUserForm
from .utils import is_admin, save_picture
from .models import Administrators, Election, Party, User
from passlib.hash import sha256_crypt

########### USERS ###########
@app.route('/')
def index():
    return render_template("users/login.html")


########### SUPERADMIN ###########
@app.route('/admin', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        admin = Administrators.query.filter_by(email=form.email.data).first()
        if admin:
            pass
        else:
            flash("Cannot find user with specified email and password", "danger")
            return redirect(url_for('admin_login'))
    return render_template("admin/login.html", form=form)


@app.route('/dashboard')
def admin_dashboard():
    elections = Election.query.all()
    return render_template("admin/dashboard.html", elections=elections)


@app.route('/create/election', methods=["POST", "GET"])
def create_election():
    form = CreateElectionForm()
    if form.validate_on_submit():
        try:
            election = Election(name=form.name.data, date_started=form.date_started.data, date_ended=form.date_ended.data)
            db.session.add(election)
            db.session.commit()
            flash('Election added successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Election already exists', 'danger')
        return redirect(url_for('create_election'))
    return render_template("admin/create_election.html", form=form)


@app.route('/delete/election/<id>')
def delete_election(id):
    try:
        Election.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Election Deleted Successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Something went wrong in deleting election', 'danger')
    return redirect(url_for('admin_dashboard'))


@app.route('/get/admins')
def get_admins():
    admins = Administrators.query.filter_by(role='admin').all()
    return render_template("admin/get_admins.html", admins=admins)


@app.route('/create/admin', methods=["POST", "GET"])
def create_admin():
    form = CreateAdminForm()
    if form.validate_on_submit():
        hashed_pass = sha256_crypt.hash(form.confirm_password.data)
        try:
            admin = Administrators(name=form.name.data, email=form.email.data, password=hashed_pass, role='admin')
            db.session.add(admin)
            db.session.commit()
            flash('Admin created successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Admin with same email exists', 'danger')
        return redirect(url_for('create_admin'))
    return render_template("admin/create_admin.html", form=form)


@app.route('/delete/admin/<id>')
def delete_admin(id):
    try:
        Administrators.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Admin Deleted Successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Something went wrong in deleting admin', 'danger')
    return redirect(url_for('get_admins'))


@app.route('/get/parties')
def get_parties():
    parties = Party.query.all()
    return render_template("admin/get_parties.html", parties=parties)


@app.route('/create/party', methods=["POST", "GET"])
def create_party():
    form = CreatePartyForm()
    if form.validate_on_submit():
        user_picture = save_picture(form.picture.data)
        logo = save_picture(form.logo.data)
        try:
            user = User(name=form.name.data, picture=user_picture, adhaar_number=form.adhaar_number.data, 
                        mobile_number=form.mobile_number.data, address=form.address.data, 
                        district=form.district.data, voter_id=form.voter_id.data, role='party')
            db.session.add(user)
            db.session.flush()
            party = Party(name=form.party_name.data, logo=logo, abbreviation=form.abbreviation.data, user_id=user.id)
            db.session.add(party)
            db.session.commit()
            flash('Successfully created party', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Something went wrong in creating party', 'danger')
        return redirect(url_for('create_party'))
    return render_template("admin/create_party.html", form=form)


@app.route('/delete/party/<id>')
def delete_party(id):
    try:
        party = Party.query.filter_by(id=id)
        user_id = party.first().user_id
        party.delete()
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        flash('Party Deleted Successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Something went wrong in deleting party', 'danger')
    return redirect(url_for('get_parties'))


@app.route('/get/users')
def get_users():
    users = User.query.all()
    return render_template("admin/get_users.html", users=users)


@app.route('/create/user', methods=["POST", "GET"])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user_picture = save_picture(form.picture.data)
        try:
            user = User(name=form.name.data, picture=user_picture, adhaar_number=form.adhaar_number.data, 
                        mobile_number=form.mobile_number.data, address=form.address.data, 
                        district=form.district.data, voter_id=form.voter_id.data)
            db.session.add(user)
            db.session.commit()
            flash('Successfully created User', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('User with current adhaar number already exists', 'danger')
        return redirect(url_for('create_user'))
    return render_template("admin/create_user.html", form=form)


@app.route('/delete/user/<id>')
def delete_user(id):
    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('User Deleted Successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Something went wrong in deleting User', 'danger')
    return redirect(url_for('get_users'))

########### PARTIES ###########


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))