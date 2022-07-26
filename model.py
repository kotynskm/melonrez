""" Data models for Melon Reservation app. """
import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """ Data model for a user. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), nullable=False, unique=True)

     # relationship to reservations
    reservations = db.relationship('Reservation', backref='user')

    def __repr__(self):
        return f'<User {self.email}, ID {self.user_id}>'

    @classmethod
    def create_user(cls, user_id, email):
        """ Create a user. """
        return cls(user_id=user_id, email=email)

    @classmethod
    def get_by_email(cls, email):
        """ Get user by email. """
        return cls.query.filter(User.email == email).first()

    @classmethod
    def get_by_id(cls, user_id):
        """ Get user by ID. """
        return cls.query.get(user_id)


class Reservation(db.Model):
    """ Data model for a reservation. """

    __tablename__ = 'reservations'

    rez_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    rez_name = db.Column(db.String)

    # relationship to user
    # reservations = db.relationship('Reservation', backref='user')

    def __repr__(self):
        return f'<Reservation {self.rez_name}, User ID {self.user_id}>'

    @classmethod
    def create_rez(cls, user_id, start_date, end_date, rez_name):
        """ Create a reservation. """
        return cls(user_id=user_id, start_date=start_date, end_date=end_date, rez_name=rez_name)



def connect_to_db(flask_app, db_uri="postgresql:///melonrez", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)