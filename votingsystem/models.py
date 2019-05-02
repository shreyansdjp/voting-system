from . import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    adhaar_number = db.Column(db.String(12), nullable=False, unique=True)
    otp = db.Column(db.Integer, nullable=True)
    mobile_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)
    district = db.Column(db.String(100), nullable=False)
    voter_id = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_started = db.Column(db.String(20), nullable=False)
    date_ended = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    logo = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    elections = db.relationship('ParitesParticipating', backref='party', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ParitesParticipating(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('election_id', 'party_id'),
    )
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ElectedParty(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('election_id', 'party_id'),
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ElectionStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    no_of_seats = db.Column(db.Integer, nullable=False)
    did_win = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Administrators(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(11), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
