import urllib2
import arrow
from bs4 import BeautifulSoup
from model import connect_to_db, db
from server import app

#sample list of restaurants based on Eater SF Brunch List, convert this to database query later on
resto_list = [1906, 4485, 15424, 19651, 20233, 35785, 37594, 43240, 43885, 52636, 97309, 102289, 114490, 141049, 144916, 148555, 148759, 160438, 160675, 211402]
temp_resto_list = [1906, 4485]
person_list = [2]


def current_time():
    """Create datetime object for current date and closest dates for Sat/Sun"""

    current_time = arrow.utcnow().to('US/Pacific')
    current_weekday = current_time.weekday()

    #check current day to get values of closest saturday and sunday
    if current_weekday < 5:
        first_sat = current_time.replace(days=+(5-current_weekday))
        first_sun = first_sat.replace(days=+1)
    elif current_weekday == 5:
        first_sat = current_time.replace(days=+7)
        first_sun = current_time.replace(days=+1)
    else:
        first_sat = current_time.replace(days=+6)
        first_sun = first_sat.replace(days=+1)

    #append first sat/sun in proper opentable URL format without changing arrow object
    final_dates = [first_sat.format('MM/DD/YYYY'), first_sun.format('MM/DD/YYYY')]

    #append 6 more dates to the final list of dates
    # for i in range(6):
    #     first_sat = first_sat.replace(days=+7)
    #     first_sun = first_sun.replace(days=+7)
    #     final_dates.append(first_sat.format('MM/DD/YYYY'))
    #     final_dates.append(first_sun.format('MM/DD/YYYY'))

    return final_dates


#create global variable of date list to be used by ot_extract function
# date_list = current_time()


def scrape_opentable(date_list, resto_list, person_list):
    """Create output HTML files of available reservations for scraping

    Loop over list for restos, persons, dates to extract all HTML files
    Sample list of filenames = ['output_08132016_1906_2.html', 'output_08132016_1906_4.html']"""

    list_of_filenames = []

    for date in date_list:
        for resto in resto_list:
            for person in person_list:
                print date, resto, person
                reservation_time ='%2012:00:00%20PM'
                date_filename = date.replace('/', '')  # strip / for filename
                url = 'http://opentable.com/opentables.aspx?t=rest&r=%i&d=%s%s&p=%i' % (resto, date, reservation_time, person)
                filename = 'output_%s_%s_%i.html' % (date_filename, resto, person)
                list_of_filenames.append(filename)
                print url
                print filename
                #create HTML files based on generated URL
                # opentable_file = urllib2.urlopen(url)
                # with open(filename, 'wb') as output:
                #     output.write(opentable_file.read())

    #generates list of filenames for Beautiful Soup scraping
    return list_of_filenames

#call scrape_opentable function, and create global variable for list of filenames to be passed to final_reservation_times functions
# list_of_filenames = scrape_opentable(date_list, resto_list, person_list)


def final_reservation_times(list_of_filenames):
    """Use Beautiful Soup to extract reservation times from html files

    Sample Filename: 'output_08132016_1906_2.html'
    Sample Output:
    {opentable_id: [persons, date, times]}
    {1906: [2, '08/13/2016', ['12:00', '01:30']]} """

    #initialize empty dictionary for final output
    reservation_dict = {}

    for outputfile in list_of_filenames:
        date = '%s/%s/%s' % (outputfile[7:9], outputfile[9:11], outputfile[11:15])
        restaurant_id = outputfile[14:]
        html_doc = open('%s' % (outputfile))
        soup = BeautifulSoup(html_doc, 'html.parser')
        available_times = soup.find_all('span', class_='t')
        final_times = []

        for x in available_times:
            final_times.append(x.text)

        #delete any blank or zero values
        final_times = filter(lambda a: a != u'\xa0', final_times)

        output_dictionary[restaurant_id] = final_times

    return reservation_dict

def load_reservations():
    """Load reservations data to database from scraped data"""

    print "Loading Reservation data"

    #Delete all rows in table to reseed data every time this function is called
    Reservation.query.delete()

    #Read the source file and insert data, use 'rU' so \r is read as line break
    for line in open('data/opentable.txt', 'rU'):
        line = line.rstrip()
        opentable_id, reserve_url, price, address, phone, lat, lng, image_url, name = line.split('|')

        reservation = Reservation(opentable_id=opentable_id,
                                  date=date,
                                  people=people
                                  time=time)

        #add opentable info to the database
        db.session.add(reservation)

    #commit work
    db.session.commit()


##############################################################################
# Helper functions

# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     # Configure to use our PstgreSQL database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurants'
#     db.app = app
#     db.init_app(app)

# if __name__ == "__main__":
#     # As a convenience, if we run this module interactively, it will leave
#     # you in a state of being able to work with the database directly.

#     from server import app
#     connect_to_db(app)
#     print "Connected to DB."


##############################################################################

# if __name__ == "__main__":
#     #run the following functions when the function is called 
#     ot_extract(ot_list)
#     create_list_of_filenames(ot_list)

