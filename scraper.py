import urllib2
import arrow
from bs4 import BeautifulSoup
from model import Opentable, Reservation, connect_to_db, db
from server import app
import json


# resto_list = [1906]
person_list = [4, 6]  # limit search options to 4 and 6 people


def restaurant_query():
    """Query database for restaurant IDs and return list of opentable IDs

    Sample Output:
    resto_list = [1906]"""

    opentable_id = db.session.query(Opentable.opentable_id).all()
    resto_list = []

    for restaurant in opentable_id:
        resto_list.append(restaurant[0])

    return resto_list


def current_time():
    """Create datetime object for current date and closest dates for Sat/Sun

    Sample Output:
    final_dates = ['08/13/2016', '08/14/2016']"""

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

    #append first sat/sun in proper opentable URL format without changing arrow datetime object
    final_dates = [first_sat.format('MM/DD/YYYY'), first_sun.format('MM/DD/YYYY')]

    # append 1 more weekend/s to the final list of dates
    for i in range(1):
        first_sat = first_sat.replace(days=+7)
        first_sun = first_sun.replace(days=+7)
        final_dates.append(first_sat.format('MM/DD/YYYY'))
        final_dates.append(first_sun.format('MM/DD/YYYY'))

    return final_dates


def scrape_opentable(date_list, resto_list, person_list):
    """Create output HTML files of available reservations for scraping

    Loop over list for restos, persons, dates to extract all HTML files
    Sample list of filenames = ['output_08132016_1906_2.html', 'output_08132016_1906_4.html']"""

    list_of_filenames = []

    for date in date_list:
        for resto in resto_list:
            for person in person_list:
                reservation_time = '%2012:00:00%20PM'
                date_filename = date.replace('/', '')  # strip / for filename
                url = 'http://opentable.com/opentables.aspx?t=rest&r=%i&d=%s%s&p=%i' % (resto, date, reservation_time, person)
                filename = 'output_%s_%s_%i.html' % (date_filename, resto, person)
                list_of_filenames.append(filename)
                #create HTML files based on generated URL
                opentable_file = urllib2.urlopen(url)
                with open('data/%s' % (filename), 'wb') as output:
                    output.write(opentable_file.read())

    #save list_of_filenames as text file
    with open('data/list_of_filenames.txt', 'wb') as output:
        output.write(str(list_of_filenames))

    #generates list of filenames for Beautiful Soup scraping
    return list_of_filenames


def reservation_times(list_of_filenames):
    """Use Beautiful Soup to extract reservation times from html files

    Sample Filename: 'output_08132016_1906_2.html'
    Sample Output:
    {opentable_id: [date, people, times]}
    {u'1906': [u'08/13/2016', u'2', [u'12:30', u'1:00', u'11:30', u'11:45']]}"""

    #initialize empty dictionary for final output
    reservation_dict = {}

    reservation_id = 1  # reservation_id is a counter to be used for dictionary key

    for outputfile in list_of_filenames:
        datestring = '%s/%s/%s' % (outputfile[7:9], outputfile[9:11], outputfile[11:15])
        html_doc = open('data/%s' % (outputfile))
        outputfile = outputfile.rstrip('.html')  # remove html before unpacking filename
        output, date, opentable_id, people = outputfile.split('_')  # unpack filename
        reservation_times = []

        # Only parse file if 'No tables available' not in html file
        if 'No tables are available' not in open('data/%s.html' % (outputfile)).read():
            soup = BeautifulSoup(html_doc, 'html.parser')  # create beautiful soup object
            available_times = soup.find_all('span', class_='t')  # get reservation times

            for x in sorted(available_times):
                if len(reservation_times) < 5:
                    x = x.text
                    x = x.rstrip(' PM')  # delete extra string from times
                    reservation_times.append(x)  # get text only from beautiful soup object
                else:
                    break
            #delete any blank or zero values
            reservation_times = filter(lambda a: a != u'\xa0', reservation_times)

        #create dictionary item for upload to database
        reservation_dict[reservation_id] = [opentable_id, datestring, people, reservation_times]

        reservation_id = reservation_id + 1

    #write reservation data to json file
    reservation_json = json.dumps(reservation_dict)
    with open('data/reservation_json.json', 'wb') as output:
        output.write(reservation_json)

    return reservation_dict


def load_reservations():
    """Load reservations data to database from scraped data"""

    print "Loading Reservation data"

    #Delete all rows in table to reseed data every time this function is called
    Reservation.query.delete()

    #open json file and convert to dictionary for looping over
    reservation_dict = json.load(open('data/reservation_json.json'))

    #loop over all items in dictionary to insert details to database
    for reservation_id, details in reservation_dict.items():
        reservation_id = reservation_id
        opentable_id = details[0]
        arrow_date = arrow.get(details[1], 'MM/DD/YYYY')  # convert string to datetime
        date = arrow_date.format('DD-MMM-YYYY')
        people = int(details[2])
        if len(details[3]) == 0:
            time = None  # if no reservations, assign Nonetype
        else:
            time = details[3]

        reservation = Reservation(reservation_id=reservation_id,
                                  opentable_id=opentable_id,
                                  date=date,
                                  people=people,
                                  time=time)

        #add opentable info to the database
        db.session.add(reservation)

    #commit work
    db.session.commit()


# #############################################################################
# Helper functions


if __name__ == "__main__":
    # User can work with database directly when run in interactive mode

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    resto_list = restaurant_query()
    print 'Creating date list'
    date_list = current_time()
    print 'Scraping open table'
    list_of_filenames = scrape_opentable(date_list, resto_list, person_list)
    print 'Creating reservation dictionary'
    reservation_times(list_of_filenames)
    print 'Seeding database'
    load_reservations()

