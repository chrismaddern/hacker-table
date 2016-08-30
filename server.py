""" Hacker Table """

import os
import json
from datetime import datetime

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

from model import Restaurant, Opentable, Reservation, User, User_Detail, connect_to_db, db
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
def index():
    """Homepage."""

    # Check if user is logged in and assign None-type
    try:
        print session['user_email']
    except:
        session['user_email'] = None
        print session['user_email']

    #query all existing reservations that are not null
    reservations = Reservation.query.filter(Reservation.time != None).order_by('date', 'people').all()

    #query unique dates in reservation database
    dates = db.session.query(Reservation.date).group_by(Reservation.date).order_by(Reservation.date).all()

    # return homepage with reservations
    return render_template("homepage2.html", reservations=reservations, dates=dates, gkey=gkey)


@app.route('/create', methods=['POST'])
def create():
    """Create Account Route"""

    #get email and password from the create account modal
    user_email = request.form.get('user_email')
    password = request.form.get('password')

    user = User.query.filter_by(user_email=user_email).first()
    if user is not None:
        flash('This user already exists.')
    else:
        user = User(user_email=user_email, password=password)
        db.session.add(user)
        flash('Your account has been created and you are logged in.')

    return redirect('/')  # redirect user to homepage


@app.route('/login', methods=['POST'])
def login():
    """Login Route"""

    #get email and password from the login modal
    user_email = request.form.get('user_email')
    password = request.form.get('password')

    user = User.query.filter_by(user_email=user_email).first()
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
    """Logout Route"""

    if session['user_email'] is None:
        flash('You are not logged in.')
    else:
        del session['user_email']
        flash('You are now logged out.')

    return redirect('/')  # redirect user to homepage

 
@app.route('/tryresto', methods=['POST'])
def tryresto():
    """Route to update database with selected user resto"""

    resto_id = request.form.get('id')
    print resto_id

    return jsonify(status="success for try", resto_id=resto_id)


@app.route('/likeresto', methods=['POST'])
def likeresto():
    """Route to update database with user like information"""

    resto_id = request.form.get('id')
    print resto_id

    return jsonify(status="like success", resto_id=resto_id)


@app.route('/dislikeresto', methods=['POST'])
def dislikeresto():
    """Route to update database with user dislike information"""

    resto_id = request.form.get('id')
    print resto_id

    return jsonify(status="dislike success", resto_id=resto_id)


@app.route('/restaurant_list')
def restaurant_list():
    """List of all Restaurants."""

    #query all restaurants in database
    restaurants = Restaurant.query.order_by('name').all()

    # print session['user_email']

    # return list of restaurants
    return render_template("restaurant_list2.html", restaurants=restaurants)


@app.route('/restaurant_details/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    """Detailed page per Restaurant."""

    #query all restaurants in database
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()

    # return detailed restaurant page
    return render_template("restaurant_details.html", restaurant=restaurant, gkey=gkey)


@app.route('/resto_markers', methods=['POST'])
def resto_markers():
    """Provide restaurant details for homepage map in JSON format"""


    #query unique dates in reservation database
    dates = db.session.query(Reservation.date).group_by(Reservation.date).order_by(Reservation.date).all()

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

    print date
    print resto
    print people

    resto_markers = db.session.query(Reservation, Opentable, Restaurant).filter(Reservation.time != None, Reservation.date.in_(date), Restaurant.name.ilike(resto), Reservation.people.in_(people)).join(Opentable).join(Restaurant).all()

    resto_dict = {}
    counter = 1
    for resto in resto_markers:
        resto_dict[counter] = {'name': resto[2].name, 'lat': resto[2].lat, 'lng': resto[2].lng}
        counter += 1

    resto_json = json.dumps(resto_dict)

    print resto_json

    return resto_json


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
