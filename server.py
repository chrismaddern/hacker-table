""" Hacker Table """

import os
import json
from datetime import datetime

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "my_secret_key"

#raise an error for undefined Jinja variables
app.jinja_env.undefined = StrictUndefined

# Run 'source secrets.sh in terminal'
# Pass Google JS API key to render_template
gkey = os.environ['GOOGLE_API_KEY']


@app.route('/')
def homepage():
    """Homepage."""

    # Check if user is logged in, if not assign None-type
    try:
        session['user_email']
    except:
        session['user_email'] = None

    return render_template("homepage.html")


@app.route('/reservations')
def reservations():
    """Reservations Page"""

    # Check if user is logged in, if not assign None-type
    try:
        session['user_email']
    except:
        session['user_email'] = None

    #query all existing reservations
    reservations = Reservation.get_all_reservations()

    #query unique dates in reservation database
    dates = Reservation.get_all_dates()

    # return homepage with reservations
    return render_template("reservations.html", reservations=reservations, dates=dates, gkey=gkey)


@app.route('/restaurant_list')
def restaurant_list():
    """List of all Restaurants."""

    #query all restaurants in database
    restaurants = Restaurant.get_all_restaurants()

    # Check if user is logged in, if not assign None-type
    try:
        session['user_email']
    except:
        session['user_email'] = None

    # Get user_id based on logged in user from session, and get details for all restaurants rated
    if session['user_email']:
        user_id = User.get_user_id(session['user_email'])
        user_details = User_Detail.get_user_details(user_id)
    else:
        user_details = None

    # return list of restaurants
    return render_template("restaurant_list.html", restaurants=restaurants, user_details=user_details)


@app.route('/restaurant_details/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    """Detailed page per Restaurant."""

    #query all restaurants in database
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()

    # return detailed restaurant page
    return render_template("restaurant_details.html", restaurant=restaurant, gkey=gkey)


@app.route('/user')
def user():
    """List of all existing user notifications"""

    # Check if user is logged in, if not assign None-type
    try:
        session['user_email']
    except:
        session['user_email'] = None

    # Get user_id based on logged in user from session
    user_id = User.get_user_id(session['user_email'])
    notifications = Notification.get_user_notifications(user_id)

    return render_template('user.html', notifications=notifications)


@app.route('/create', methods=['POST'])
def create():
    """Create Account"""

    #get email and password from the create account modal
    user_email = request.form.get('user_email')
    password = request.form.get('password')

    user = User.search_user(user_email, password)

    if user is None:
        user = User(user_email=user_email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_email'] = user.user_email
        flash('A new user has been created')
    else:
        flash('This user already exists')

    return redirect('/')  # redirect user to homepage


@app.route('/notify', methods=['POST'])
def notify():
    """Create Notification for Reservation"""

    opentable_id = int(request.form.get('opentable'))
    date = request.form.get('date')
    date = datetime.strptime('2016 ' + date, '%Y %b%d')
    people = int(request.form.get('people'))
    user_mobile = request.form.get('user_mobile')

    # If mobile provided, update user mobile in database
    if user_mobile:
        User.update_mobile(session['user_email'], user_mobile)

    # Get user_id based on logged in user from session
    user_id = User.get_user_id(session['user_email'])

    msg = Notification.add_notification(user_id, opentable_id, date, people)
    flash(msg)

    return redirect('/reservations')  # redirect user to reservations page


@app.route('/cancel', methods=['POST'])
def cancel():
    """Delete notification from database"""

    opentable_id = int(request.form.get('opentable'))
    date = request.form.get('date')
    people = int(request.form.get('people'))

    # Get user_id based on logged in user from session
    user_id = User.get_user_id(session['user_email'])

    msg = Notification.delete_notification(user_id, opentable_id, date, people)
    flash(msg)

    return redirect('/user')  # redirect user to user page


@app.route('/login', methods=['POST'])
def login():
    """Login User"""

    #get email and password from the login modal
    user_email = request.form.get('user_email')
    password = request.form.get('password')

    user = User.search_user(user_email)
    if user is None:
        flash('This user does not exist.')
    else:
        if user.password == password:
            session['user_email'] = user.user_email  # add user email to session
            flash('You have successfully logged in.')
        else:
            flash('Your password is incorrect.')

    return redirect('/')  # redirect user to homepage


@app.route('/logout')
def logout():
    """Logout User"""

    if session['user_email'] is None:
        flash('You are not logged in.')
    else:
        del session['user_email']
        flash('You are now logged out.')

    return redirect('/')  # redirect user to homepage


@app.route('/update_status', methods=['POST'])
def update_status():
    """Route to update database with selected user resto"""

    # Unpack values from form
    restaurant_id = request.form.get('id')
    status = request.form.get('status')

    # Get user_id based on logged in user from session
    user_id = User.get_user_id(session['user_email'])

    # Check if user has already made selection for specified restaurant
    user_detail = User_Detail.search_user_detail(user_id, restaurant_id)

    # if entry does not exist, add to database
    if user_detail is None:
        db.session.add(User_Detail(user_id=user_id, restaurant_id=restaurant_id, status=status))
        db.session.commit()
    # if new status equivalent to existing status, set as None
    elif user_detail.status == status:
        query.update({'status': None})
        db.session.commit()
    # replace existing status with new status
    else:
        query.update({'status': status})
        db.session.commit()

    return jsonify(status=status, resto_id=restaurant_id)


@app.route('/resto_markers', methods=['POST'])
def resto_markers():
    """Provide restaurant details for homepage map in JSON format"""

    #query unique dates in reservation database
    dates = Reservation.get_all_dates()

    #parse form inputs for query
    date = request.form.get("date")
    resto = request.form.get("resto")
    people = request.form.get("people")

    if date == "":
        date = dates
    else:
        date = [datetime.strptime('2016 ' + date, '%Y %b %d, %a')]

    if resto == "":
        resto = '%'
    else:
        resto = "%"+resto+"%"

    if people == "":
        people = [2, 4, 6]
    else:
        people = [int(people)]

    resto_markers = db.session.query(Reservation, Opentable, Restaurant).filter(Reservation.time != None, Reservation.date.in_(date), Restaurant.name.ilike(resto), Reservation.people.in_(people)).join(Opentable).join(Restaurant).all()

    resto_dict = {}
    counter = 1
    for resto in resto_markers:
        resto_dict[counter] = {'name': resto[2].name, 'lat': resto[2].lat, 'lng': resto[2].lng}
        counter += 1

    resto_json = json.dumps(resto_dict)
    return resto_json


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')
