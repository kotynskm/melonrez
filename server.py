from flask import Flask, render_template, request, session, redirect, jsonify, flash
import requests
from model import User, Reservation, connect_to_db, db
from datetime import date, datetime, timedelta
from random import choice
import json

RESERVATIONS = [{'date': '2022-07-26', 'time': '18:00:00', 'name': 'Cantaloupe Tasting'}, {'date': '2022-08-26', 'time': '19:00:00', 'name': 'Watermelon Tasting'},
{'date': '2022-08-01', 'time': '16:00:00', 'name': 'Durian Tasting'},{'date': '2022-09-15', 'time': '15:00:00', 'name': 'Densuke Tasting'}]

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
    data = []
    date = request.args.get('start_date')

    for res in RESERVATIONS:
        if res['date'] == date:
            data.append({'date': res['date'], 'time': res['time'], 'name': res['name']})
            
    return render_template('reservations.html', data=data)

# --- add reservation to user ---
@app.route('/create_rez', methods=['POST'])
def create_reservation():
    """ Create a reservation for the user. """
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    user_reservations = user.reservations
    date_list = []

    # add user's reservation dates to a list
    for rez in user_reservations:
        date_list.append(rez.start_date.strftime('%Y-%m-%d'))
    # get the date from the form for the new reservation
    res = request.form.get('reservation')
    info = res.split(',')
    res_date = info[0]
    # check if the new reservation date is in the user's date list
    if res_date in date_list:
        flash("That reservation already exists! Sorry, please try another date.")
        return redirect('/homepage')
    else:
        reservation = Reservation.create_rez(user_id, info[0], info[1], info[2])
        db.session.add(reservation)
        db.session.commit()
        
        return redirect('/homepage')

# --- add reservation to calendar ---
@app.route('/update_calendar')
def display_reservations():
    """ Get JSON data for calendar. """
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    reservations = []

    for res in user.reservations:
        
        reservations.append({
            'title': res.rez_name,
            'start': res.start_date.strftime("%Y-%m-%d")
        })
    
    return jsonify(reservations)

# --- go back to homepage ---
@app.route('/home')
def return_home():
    """ Return to the homepage. """

    return redirect('/homepage')

# --- delete a reservation ---
@app.route('/delete_rez', methods=['POST'])
def delete_rez():
    """ Delete a reservation. """
    rez_id = request.form.get('rez_id')

    reservation = Reservation.get_by_id(rez_id)

    db.session.delete(reservation)
    db.session.commit()

    return redirect('/homepage')


if __name__ == '__main__':
    connect_to_db(app)
    app.run (debug=True, host='0.0.0.0')