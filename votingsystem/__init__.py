from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i know i know'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/voting_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from . import routes
