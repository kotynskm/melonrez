from flask import Flask, render_template, request, session, redirect, jsonify, flash
import requests
from model import User, Reservation, connect_to_db, db
from datetime import datetime, timedelta
from random import choice
import json

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# --- login route --- 
@app.route('/')
def login_page():
    """ View the login page. """

    return render_template('login.html')




if __name__ == '__main__':
    connect_to_db(app)
    app.run (host='0.0.0.0')