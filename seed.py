"""Utility file to seed restaurants database in seed_data"""

from model import Restaurant, Opentable, Yelp_Detail, User, User_Detail
from model import connect_to_db, db
from server import app
import json


def load_opentable():
    """Load opentable data to database from opentable.txt file"""

    print "Loading Opentable data"

    #Delete all rows in table to reseed data every time this function is called
    Opentable.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('seed/opentable.csv', 'rU'):
        line = line.rstrip()
        opentable_id, name = line.split(',')

        opentable = Opentable(opentable_id=opentable_id,
                              name=name)

        #add opentable info to the database
        db.session.add(opentable)

    #commit work
    db.session.commit()


def load_restaurants():
    """Load restaurants into database from restaurant.txt file"""

    print "Loading Restaurants"

    #Delete all rows in table to reseed data every time this function is called
    Restaurant.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('seed/restaurants.csv', 'rU'):
        line = line.rstrip()
        name, opentable_id, eater, yelp, timeout, zagat, michelin, infatuation, lat, lng = line.split(',')
        if opentable_id == 'None':
            opentable_id = None

        #create restaurant object based on inputs from the line
        restaurant = Restaurant(name=name,
                                opentable_id=opentable_id,
                                eater=eater,
                                yelp=yelp,
                                timeout=timeout,
                                zagat=zagat,
                                michelin=michelin,
                                infatuation=infatuation,
                                lat=lat,
                                lng=lng)

        #add restaurant to the database
        db.session.add(restaurant)

    #commit work
    db.session.commit()


def load_yelp_details():
    """Load detailed information on restaurants from yelp api"""

    print "Loading Yelp Details"

    #Delete all rows in table to reseed data every time this function is called
    Yelp_Detail.query.delete()

    yelp_dict = json.load(open('seed/yelp_data.json'))

    for resto, details in yelp_dict.items():
        resto_name = resto
        yelp_id, yelp_name, image_url, display_phone, review_count, categories, rating, address, city, neighborhoods, lat, lng, reservation_url = details
        if reservation_url == 'None':
            reservation_url = None

        #create table entry for yelp detail
        yelp_detail = Yelp_Detail(resto_name=resto_name,
                                  yelp_id=yelp_id,
                                  yelp_name=yelp_name,
                                  image_url=image_url,
                                  display_phone=display_phone,
                                  review_count=review_count,
                                  categories=categories,
                                  rating=rating,
                                  address=address,
                                  city=city,
                                  neighborhoods=neighborhoods,
                                  lat=lat,
                                  lng=lng,
                                  reservation_url=reservation_url)

        #add yelp detail to the database
        db.session.add(yelp_detail)

    #commit work
    db.session.commit()


def load_users():
    """Load sample users to database"""

    print "Loading Users"

    #Delete all rows in table to reseed data every time this function is called
    User.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('seed/users.csv', 'rU'):
        line = line.rstrip()
        user_email, password = line.split(',')

        #create user object based on inputs from the line
        user = User(user_email=user_email, password=password)

        #add user to the database
        db.session.add(user)

    #commit work
    db.session.commit()


def load_user_details():
    """Load sample user feedback to database"""

    print "Loading User Details"

    #Delete all rows in table to reseed data every time this function is called
    User_Detail.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('seed/user_details.csv', 'rU'):
        line = line.rstrip()
        user_id, opentable_id, have_tried, want_to_try, like_resto = line.split(',')

        # Convert fields with 'None' to None-type
        if have_tried == 'None':
            have_tried = None
        if want_to_try == 'None':
            want_to_try = None
        if like_resto == 'None':
            like_resto = None

        #create user object based on inputs from the line
        user_details = User_Detail(user_id=user_id,
                                   opentable_id=opentable_id,
                                   have_tried=have_tried,
                                   want_to_try=want_to_try,
                                   like_resto=like_resto)

        #add user to the database
        db.session.add(user_details)

    #commit work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_opentable()
    load_restaurants()
    load_yelp_details()
    load_users()
    load_user_details()
