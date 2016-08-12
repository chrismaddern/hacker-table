""" Hacker Table """

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


@app.route('/')
def index():
    """Homepage."""

    #query all existing reservations that are not null
    reservations = Reservation.query.filter(Reservation.time != None).order_by('date', 'people').all()

    # return 'Hello world'
    return render_template("homepage.html", reservations=reservations)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host= '0.0.0.0')
