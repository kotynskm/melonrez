"""Script to seed database."""

import os
import json
from datetime import datetime

import model
import server

os.system("dropdb melonrez")
os.system("createdb melonrez")

model.connect_to_db(server.app)
model.db.create_all()


def load_users():
    """ Load users into the database. """

    kailey = model.User.create_user(user_id=1, email='kk@gmail.com')
    omkar = model.User.create_user(user_id=2, email='om@gmail.com')

    model.db.session.add_all([kailey, omkar])
    model.db.session.commit()

def load_reservations():
    """ Load reservations into the database. """
    
    cantaloupe = model.Reservation.create_rez(user_id=1, start_date=datetime.strptime("2022-08-01", "%Y-%m-%d"), rez_name="cantaloupes")

    model.db.session.add_all(cantaloupe)
    model.db.session.commit()

load_users()

