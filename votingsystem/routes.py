from . import app, db
from flask import render_template, url_for, flash, redirect, flash, request, session
from .forms import AdminLoginForm, CreateElectionForm, CreateAdminForm, CreatePartyForm, CreateUserForm, GetAdhaarForm, VerifyOTPForm
from .utils import save_picture, is_admin, is_super_admin, logged_in, is_logged_in, current_date
from .models import Administrators, Election, Party, User, ParitesParticipating, ElectedParty
from random import randint
from passlib.hash import sha256_crypt
from datetime import datetime


@app.route('/', methods=["POST", "GET"])
@is_logged_in
def index():
    form = GetAdhaarForm()
    if form.validate_on_submit():
        user = User.query.filter_by(adhaar_number=form.adhaar_number.data).first()
        if not user:
            flash('User with specified adhaar number does not exists', 'danger')
        user.otp = randint(1000, 9999)
        db.session.commit()
        flash('Adhaar number found.. Please verify the OTP sent on your mobile', 'success')
        return redirect(url_for('verify', adhaar_number=form.adhaar_number.data))
    return render_template("user/login.html", form=form)


@app.route('/verify/<adhaar_number>', methods=["POST", "GET"])
@is_logged_in
def verify(adhaar_number):
    form = VerifyOTPForm(adhaar_number=adhaar_number)
    if form.validate_on_submit():
        user = User.query.filter_by(adhaar_number=adhaar_number).first()
        if user:
            if user.otp == form.otp.data:
                user.otp = None
                db.session.commit()
                session['id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                session['picture'] = user.picture
                session['adhaar_number'] = user.adhaar_number
                session['voter_id'] = user.voter_id
                flash('Successfully logged in', 'success')
            else:
                flash('OTP is wrong', 'danger')
                return redirect(url_for('index'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('index'))
        return redirect(url_for('user_dashboard'))
    form.adhaar_number.data = adhaar_number
    return render_template("user/verify.html", form=form)


########### USERS ###########
@app.route('/user/dashboard')
@logged_in
def user_dashboard():
    elections = Election.query.all()
    for election in elections:
        elected_party = ElectedParty.query.filter_by(election_id=election.id, user_id=session.get('id')).first()
        if elected_party:
            election.voted_for = True
        else:
            election.voted_for = False
    date = current_date().strftime("%Y-%m-%d")
    return render_template("user/dashboard.html", elections=elections, current_date=date)


@app.route('/user/vote/<election_id>')
@logged_in
def user_vote(election_id):
    participating_parties = ParitesParticipating.query.filter_by(election_id=election_id).all()
    parties = []
    for party in participating_parties:
        parties.append(Party.query.filter_by(id=party.party_id).first())
    print(parties)
    return render_template("user/vote.html", parties=parties, election_id=election_id)


@app.route('/elect/party/<election_id>/<party_id>')
@logged_in
def elect_party(election_id, party_id):
    elected_party = ElectedParty.query.filter_by(election_id=election_id, party_id=party_id).first()
    if not elected_party:
        try:
            elect_party = ElectedParty(election_id=election_id, party_id=party_id, user_id=session.get('id'))
            db.session.add(elect_party)
            db.session.commit()
            flash('Successfully voted', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Something went wrong in electing the party', 'danger')
        return redirect(url_for('user_dashboard'))
    else:
        if elected_party.user_id == session.get('id'):
            flash('You have already voted for this party', 'danger')
        else:
            try:
                elect_party = ElectedParty(election_id=election_id, party_id=party_id, user_id=session.get('id'))
                db.session.add(elect_party)
                db.session.commit()
                flash('Successfully voted', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Something went wrong in electing the party', 'danger')
        return redirect(url_for('user_dashboard'))



########### PARTIES ###########
@app.route('/party/dashboard')
@logged_in
def party_dashboard():
    return render_template("party/dashboard.html")


########### SUPERADMIN ###########
@app.route('/admin', methods=["POST", "GET"])
@is_logged_in
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        admin = Administrators.query.filter_by(email=form.email.data).first()
        print(admin.password)
        if admin:
            if sha256_crypt.verify(form.password.data, admin.password):
                session['id'] = admin.id
                session['role'] = admin.role
                flash('Successfully Logged In', 'success')
                if admin.role == 'admin':
                    return redirect(url_for('get_users'))
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Password is wrong', 'danger')
                return redirect(url_for('admin_login'))
        else:
            flash("Cannot find user with specified email and password", "danger")
            return redirect(url_for('admin_login'))
    return render_template("admin/login.html", form=form)


@app.route('/dashboard')
@logged_in
@is_super_admin
def admin_dashboard():
    elections = Election.query.all()
    return render_template("admin/dashboard.html", elections=elections)


@app.route('/create/election', methods=["POST", "GET"])
@logged_in
@is_super_admin
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
@logged_in
@is_super_admin
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
@logged_in
@is_super_admin
def get_admins():
    admins = Administrators.query.filter_by(role='admin').all()
    return render_template("admin/get_admins.html", admins=admins)


@app.route('/create/admin', methods=["POST", "GET"])
@logged_in
@is_super_admin
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
@logged_in
@is_super_admin
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
@logged_in
@is_admin
def get_parties():
    parties = Party.query.all()
    return render_template("admin/get_parties.html", parties=parties)


@app.route('/create/party', methods=["POST", "GET"])
@logged_in
@is_admin
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
@logged_in
@is_admin
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
@logged_in
@is_admin
def get_users():
    users = User.query.all()
    return render_template("admin/get_users.html", users=users)


@app.route('/create/user', methods=["POST", "GET"])
@logged_in
@is_admin
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
@logged_in
@is_admin
def delete_user(id):
    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('User Deleted Successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Something went wrong in deleting User', 'danger')
    return redirect(url_for('get_users'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))