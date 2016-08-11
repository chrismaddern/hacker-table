"""Models and database functions for Hacker Brunch."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Model definitions

class Restaurant(db.Model):
    """Master list of restaurants"""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opentable_id = db.Column(db.Integer, db.ForeignKey('opentable.opentable_id'), nullable=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    eater = db.Column(db.Boolean, nullable=False)
    yelp = db.Column(db.Boolean, nullable=False)
    timeout = db.Column(db.Boolean, nullable=False)
    zagat = db.Column(db.Boolean, nullable=False)
    michelin = db.Column(db.Boolean, nullable=False)
    infatuation = db.Column(db.Boolean, nullable=False)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant opentable=%i name=%s>" % (self.opentable_id, self.name)


class Opentable(db.Model):
    """Table containing additional information from opentable"""

    __tablename__ = "opentable"

    opentable_id = db.Column(db.Integer, unique=True, nullable=True, primary_key=True)
    reserve_url = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant opentable=%i name=%s>" % (self.opentable_id, self.name)


    #define relationship between tables
    restaurants = db.relationship('Restaurant', backref=db.backref('opentable'))
    reservations = db.relationship('Reservation', backref=db.backref('opentable'))


class Reservation(db.Model):
    """Table containing available reservation times"""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opentable_id = db.Column(db.Integer, db.ForeignKey('opentable.opentable_id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    people = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Text, nullable=True)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant opentable=%i date=%s>" % (self.opentable_id, self.date)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurants'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
