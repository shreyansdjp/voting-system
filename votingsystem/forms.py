from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileAllowed
from .models import Election, Administrators, Party, User
from .utils import current_date

class AdminLoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateElectionForm(FlaskForm):
    name = StringField('Name of Election', validators=[DataRequired(), Length(min=3, max=200)])
    date_started = DateField('Date Started', format='%Y-%m-%d')
    date_ended = DateField('Date Ended', format='%Y-%m-%d')
    submit = SubmitField('Create Election')

    def validate_name(self, name):
        election = Election.query.filter_by(name=name.data).first()
        if election:
            raise ValidationError('This Election name is already taken')

    def validate_date_started(self, date_started):
        date_ended = self.date_ended.data
        if date_started.data == date_ended:
            raise ValidationError('Date Started and Date ended cannot be same')

    def validate_date_ended(self, date_ended):
        date_started = self.date_started.data
        if date_ended.data == current_date():
            raise ValidationError('Date Ended cannot be today')

        if date_ended.data < date_started:
            raise ValidationError('Date ended cannot be bigger than Date Started')


class CreateAdminForm(FlaskForm):
    name = StringField('Name of Admin', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Admin')

    def validate_email(self, email):
        admin = Administrators.query.filter_by(email=email.data).first()

        if admin:
            raise ValidationError('Admin email address already exists')


class CreatePartyForm(FlaskForm):
    name = StringField('Name of User', validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Picture of User', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    adhaar_number = StringField('Adhaar Number', validators=[DataRequired(), Length(min=12, max=12)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    voter_id = StringField('Voter ID Number', validators=[DataRequired(), Length(min=5)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5)])
    district = StringField('District', validators=[DataRequired(), Length(min=2)])
    party_name = StringField('Name of Party', validators=[DataRequired(), Length(min=2, max=20)])
    abbreviation = StringField('Short form of name', validators=[DataRequired(), Length(min=2, max=10)])
    logo = FileField('Logo of Party', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Party')

    def validate_adhaar_number(self, adhaar_number):
        user = User.query.filter_by(adhaar_number=adhaar_number.data).first()

        if user:
            raise ValidationError('user with adhaar number already exists')

    def validate_name(self, name):
        party = Party.query.filter_by(name=name.data).first()

        if party:
            raise ValidationError('Party name already exists')


class CreateUserForm(FlaskForm):
    name = StringField('Name of User', validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Picture of User', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    adhaar_number = StringField('Adhaar Number', validators=[DataRequired(), Length(min=12, max=12)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    voter_id = StringField('Voter ID Number', validators=[DataRequired(), Length(min=5)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5)])
    district = StringField('District', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Create User')

    def validate_adhaar_number(self, adhaar_number):
        user = User.query.filter_by(adhaar_number=adhaar_number.data).first()

        if user:
            raise ValidationError('user with adhaar number already exists')
    

class GetAdhaarForm(FlaskForm):
    adhaar_number = StringField('Adhaar Number', validators=[DataRequired(), Length(min=12, max=12)])
    submit = SubmitField('Verify Adhaar Number')


class VerifyOTPForm(FlaskForm):
    adhaar_number = StringField('Adhaar Number', validators=[DataRequired(), Length(min=12, max=12)])
    otp = IntegerField('Verify OTP', validators=[DataRequired()])
    submit = SubmitField('Verify OTP')
