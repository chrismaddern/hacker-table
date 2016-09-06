# Hacker Brunch

Project description
------
Hacker Brunch shows available restaurant reservations for curated list of highly sought after brunch spots in San Francisco (as lauded by Eater, Infatuation, Zagat, Michelin Guide, Yelp, Timeout). Opentable does not have an available API so Hacker Brunch uses a web scraper that uses the Beautiful Soup library to look up available reservations for the next 4 weekends for groups of 2, 4 or 6 people.

Tech Stack
------
* Python, Javascript, jQuery, Jinja, Flask, Bootstrap, HTML/CSS, Posgresql, SQLAlchemy
* APIs used: Yelp, Google Maps, Twilio

Features
------
* **_Restaurant List_** - Restaurants available on Hacker Brunch, with a link to the Yelp page of each, and information on neighborhood and cuisine
* **_Reservation List_** - Available Opentable reservations for the coming weekends; users can populate a Google Map to see markers for restaurants with reservation availability
* **_User Feedback on Restaurants_** - When a user is logged in, they have the option to save their feedback for each restaurant in the "Restaurant" page ('want to try', 'like', or 'dislike')
* **_User Notifications_** - When a user is logged in, they can set up notifications for restaurants that don't currently have available reservations so they can receive a text message as soon as a reservation for that restaurant, time and number of people is available

Screen Shots
------

**Homepage**

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/homepage.png' height=300px>

**Restaurants**

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/restaurants.png' height=300px>

**Reservations**

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/reservations.png' height=300px>

**Google Map**

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/googlemap.png' height=300px>

**Notifications**

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/notification.png' height=300px>
