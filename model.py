"""Models and database functions for Hacker Brunch."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant name=%s>" % (self.name)

    #define relationship between tables
    yelp_details = db.relationship('Yelp_Detail', backref=db.backref('restaurants'))

    @classmethod
    def get_all_restaurants(cls):
        """Get all restaurants in database"""

        restaurants = Restaurant.query.order_by('name').all()
        return restaurants


class Opentable(db.Model):
    """Table containing additional information from opentable"""

    __tablename__ = "opentable"

    opentable_id = db.Column(db.Integer, unique=True, nullable=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant name=%s>" % (self.name)


    #define relationship between tables
    restaurants = db.relationship('Restaurant', backref=db.backref('opentable'))
    reservations = db.relationship('Reservation', backref=db.backref('opentable'))
    notifications = db.relationship('Notification', backref=db.backref('opentable'))


    @classmethod
    def get_all_opentable_ids(cls):
        """Get all opentable ids in database"""

        opentable_id = db.session.query(Opentable.opentable_id).all()
        return opentable_id


class Reservation(db.Model):
    """Table containing available reservation times"""

    __tablename__ = "reservations"

    reservation_id = db.Column(db.Integer, primary_key=True)
    opentable_id = db.Column(db.Integer, db.ForeignKey('opentable.opentable_id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Text, nullable=True)

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant opentable=%i date=%s>" % (self.opentable_id, self.date)

    @classmethod
    def get_all_reservations(cls):
        """Get all reservations in database"""

        reservations = Reservation.query.order_by('date', 'people').all()
        return reservations

    @classmethod
    def get_all_dates(cls):
        """Get all dates in database"""

        dates = db.session.query(Reservation.date).group_by(Reservation.date).order_by(Reservation.date).all()
        return dates


class Yelp_Detail(db.Model):
    """Table containing restaurant details from Yelp API"""

    __tablename__ = "yelp_details"

    resto_name = db.Column(db.String(100), db.ForeignKey('restaurants.name'), primary_key=True)
    yelp_id = db.Column(db.String(100), nullable=False)
    yelp_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    display_phone = db.Column(db.String(100), nullable=False)
    review_count = db.Column(db.Integer, nullable=False)
    categories = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    neighborhoods = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    reservation_url = db.Column(db.String(100))

    #return details on object in terminal
    def __repr__(self):
        return "<Restaurant name=%s>" % (self.resto_name)


class User(db.Model):
    """Table containing User login information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(50), nullable=False)
    user_phone = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(50), nullable=False)

    #return details on object in terminal
    def __repr__(self):
        return "<Email Address=%s>" % (self.user_email)

    #define relationship between tables
    notifications = db.relationship('Notification', backref=db.backref('user'))
    user_details = db.relationship('User_Detail', backref=db.backref('user'))

    @classmethod
    def get_user_id(cls, user_email):
        """Get user_id based on session login details"""

        user_id = db.session.query(User).filter_by(user_email=user_email).one().user_id
        return user_id

    @classmethod
    def search_user(cls, user_email):
        """See if user exists in database"""

        user = User.query.filter_by(user_email=user_email).first()
        return user


    @classmethod
    def update_mobile(cls, user_email, user_mobile):
        """Update user_mobile in database"""

        db.session.query(User).filter_by(user_email=user_email).update({'user_phone': user_mobile})
        db.session.commit()


class User_Detail(db.Model):
    """Table containing user feedback on restaurants"""

    __tablename__ = "user_details"

    user_detail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    status = db.Column(db.String(10), nullable=True)

    #return details on object in terminal
    def __repr__(self):
        return "<User ID=%s>" % (self.user_id)

    @classmethod
    def get_user_details(cls, user_id):
        """Get user details based on session login details"""

        user_details = db.session.query(User_Detail).filter(User_Detail.user_id==user_id, User_Detail.status!=None).all()
        return user_details

    @classmethod
    def search_user_detail(cls, user_id, restaurant_id):
        """See if database entry exists for specified criteria"""
        user_detail = db.session.query(User_Detail).filter(User_Detail.user_id == user_id, User_Detail.restaurant_id == restaurant_id).first()
        return user_detail


class Notification(db.Model):
    """Table containing notifications for reservations"""

    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    opentable_id = db.Column(db.Integer, db.ForeignKey('opentable.opentable_id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    people = db.Column(db.Integer, nullable=False)

    #return details on object in terminal
    def __repr__(self):
        return "<Notification ID=%s>" % (self.notification_id)

    @classmethod
    def get_user_notifications(cls, user_id):
        """Get notifications based on session login details"""

        notifications = db.session.query(Notification).filter_by(user_id=user_id).all()
        return notifications

    @classmethod
    def add_notification(cls, user_id, opentable_id, date, people):
        """See if notification exists in database"""

        notification = db.session.query(Notification).filter(Notification.user_id == user_id, Notification.opentable_id == opentable_id, Notification.date == date, Notification.people == people).first()

        if notification is not None:
            return 'You already have an existing notification set up.'
        else:
            new_notification = Notification(user_id=user_id, opentable_id=opentable_id, date=date, people=people)
            db.session.add(new_notification)
            db.session.commit()
            return 'You have successfully created a notification.'

    @classmethod
    def delete_notification(cls, user_id, opentable_id, date, people):
        """See if notification exists in database"""

        db.session.query(Notification).filter(Notification.user_id == user_id, Notification.opentable_id == opentable_id, Notification.date == date, Notification.people == people).delete()
        db.session.commit()
        return 'You have deleted a notification'


def example_data():
    """Sample data for test db"""
    restaurant = Restaurant(restaurant_id=1, opentable_id=1234, name='1300 on Fillmore', eater=True, yelp=True, timeout=True, zagat=True, michelin=True, infatuation=True, lat=37.781577, lng=-122.432174)
    opentable = Opentable(opentable_id=1234, name='1300 on Fillmore')
    reservation = Reservation(reservation_id=1000, opentable_id=1234, date=datetime(2016, 9, 9, 0, 0), people=4, time='{11:00,12:15,1:30}')
    yelp_detail = Yelp_Detail(resto_name='1300 on Fillmore', yelp_id='1300', yelp_name='1300 on Fillmore', image_url='https://s3-media3.fl.yelpcdn.com/bphoto/g59iWWw05swHVr7zg3-Ixg/ms.jpg', display_phone='+1-415-771-7100', review_count=500, categories='Lounges, American (New), Venues & Event Spaces', rating=3.5, address='1300 Fillmore St Fillmore San Francisco, CA 94115', city='San Francisco', neighborhoods='Fillmore Western Addition', lat=37.781577, lng=-122.432174, reservation_url=None)
    user = User(user_id=1, user_email='tina@gmail.com', user_phone=123456, password='password')
    user_detail = User_Detail(user_id=1, restaurant_id=1, status='try')
    notification = Notification(user_id=1, opentable_id=1234, date=datetime(2016, 9, 9, 0, 0), people=6)
    db.session.add_all([restaurant, opentable, reservation, yelp_detail, user, user_detail, notification])
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///restaurants"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    # db.create_all()  # create all tables
    print "Connected to DB."
