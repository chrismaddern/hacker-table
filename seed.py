"""Utility file to seed restaurants database in seed_data"""

from model import Restaurant, Opentable, Yelp_Detail
from model import connect_to_db, db
from server import app
import json


def load_opentable():
    """Load opentable data to database from opentable.txt file"""

    print "Loading Opentable data"

    #Delete all rows in table to reseed data every time this function is called
    Opentable.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('seed/opentable.txt', 'rU'):
        line = line.rstrip()
        opentable_id, reserve_url, price, address, phone, lat, lng, image_url, name = line.split('|')

        opentable = Opentable(opentable_id=opentable_id,
                              reserve_url=reserve_url,
                              price=price,
                              address=address,
                              phone=phone,
                              lat=lat,
                              lng=lng,
                              image_url=image_url,
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
        name, opentable_id, eater, yelp, timeout, zagat, michelin, infatuation = line.split(',')
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
                                infatuation=infatuation)

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

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_opentable()
    # load_restaurants()
    load_yelp_details()
