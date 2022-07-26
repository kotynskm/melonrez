from flask import Flask, render_template, request, session, redirect, jsonify, flash
import requests
from model import User, Reservation, connect_to_db, db
from datetime import datetime, timedelta
from random import choice
import json

reservation_list = ['2022-07-26']

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# --- login route --- 
@app.route('/')
def login_page():
    """ View the login page. """

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """ Log user in and display the homepage. """
    email = request.form.get('email')
    user = User.get_by_email(email)

    session['user_id'] = user.user_id

    return redirect('/homepage')

# --- display homepage for user ---
@app.route('/homepage')
def user_page():
    """ Display users homepage. """
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    return render_template('homepage.html', user=user)

# --- calendar display ---
@app.route('/calendar')
def show_calendar():
    """ View calendar page. """

    return render_template('calendar.html')

# --- search reservations ---
@app.route('/search')
def get_reservations():
    date = request.args.get('start_date')
    # convert date string to date
    date_converted = datetime.strptime(date, '%Y-%m-%d')
    print(date)
    print(date_converted)

    return render_template('reservations.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run (host='0.0.0.0')