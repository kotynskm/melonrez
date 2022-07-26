""" File to seed database. """
from datetime import datetime
import os
from server import app
from model import User, Reservation, connect_to_db, db


def load_users():
    """ Load users into the database. """

    kailey = User.create_user(user_id=1, email='kk@gmail.com')
    omkar = User.create_user(user_id=2, email='om@gmail.com')

    db.session.add_all(kailey, omkar)
    db.session.commit()

def load_reservations():
    """ Load reservations into the database. """
    
    cantaloupe = Reservation.create_rez(user_id=1, start_date=datetime.strptime("2022-08-01", "%Y-%m-%d"), end_date=datetime.strptime("2022-08-02", "%Y-%m-%d"), rez_name="cantaloupes")

    db.session.add_all(cantaloupe)
    db.session.commit()


if __name__ == "__main__":
    os.system('dropdb melonrez')
    os.system('createdb melonrez')

    connect_to_db(app)
    db.create_all()

    load_users()
    load_reservations()