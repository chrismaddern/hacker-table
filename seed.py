"""Utility file to seed restaurants database in seed_data"""

from model import Restaurant
from model import Opentable
from model import connect_to_db, db
from server import app


def load_opentable():
    """Load opentable data to database from opentable.txt file"""

    print "Loading Opentable data"

    Opentable.query.delete()

    for line in open('data/opentable.txt','rU'):
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

        db.session.add(opentable)

    db.session.commit()


def load_restaurants():
    """Load restaurants into database from restaurant.csv file"""

    print "Loading Restaurants"

    #Delete all rows in table to reseed data every time this function si called
    Restaurant.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('data/restaurants.txt','rU'):
        line = line.rstrip()
        name, opentable_id, eater, yelp, timeout, zagat, michelin, infatuation = line.split('|')
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


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_opentable()
    load_restaurants()

