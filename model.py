from flask import Flask
from flask_login import UserMixin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:11111111@localhost:3306/WEB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)



class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name


class Auditorium(db.Model):
    __tablename__ = 'auditorium'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Booking(db.Model):
    __tablename__ = 'booking'
    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey(Users.uid, ondelete="cascade"), nullable=False)
    auditorium_uid = db.Column(db.Integer, db.ForeignKey(Auditorium.uid, ondelete="cascade"), nullable=False)
    booking_date_start = db.Column(db.DateTime, nullable=False)
    booking_date_final = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_uid, auditorium_uid, booking_date_start, booking_date_final):
        self.user_uid = user_uid
        self.auditorium_uid = auditorium_uid
        self.booking_date_start = booking_date_start
        self.booking_date_final = booking_date_final



