""" Hacker Table """

import os
import json

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import Restaurant, Opentable, Reservation, connect_to_db, db
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

    #query all existing reservations that are not null
    reservations = Reservation.query.filter(Reservation.time != None).order_by('date', 'people').all()

    # return homepage with reservations
    return render_template("homepage.html", reservations=reservations)


@app.route('/restaurant_list')
def restaurant_list():
    """List of all Restaurants."""

    #query all restaurants in database
    restaurants = Restaurant.query.order_by('name').all()

    # return list of restaurants
    return render_template("restaurant_list.html", restaurants=restaurants)


@app.route('/restaurant_details/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    """Detailed page per Restaurant."""

    #query all restaurants in database
    restaurant = db.session.query(Restaurant).filter_by(restaurant_id=restaurant_id).one()

    # return detailed restaurant page
    return render_template("restaurant_details.html", restaurant=restaurant, gkey=gkey)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
