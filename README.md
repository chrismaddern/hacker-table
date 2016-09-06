# Hacker Brunch
Hacker Brunch is a web app that solves the perennial weekend problem of finding a great brunch spot in San Francisco, without the long wait times. 

Hacker Brunch shows available Opentable restaurant reservations for a curated list of highly sought after brunch spots in San Francisco (as written about on popular food blogs and websites like Eater, Infatuation, Zagat, Michelin Guide, Yelp, Timeout). Opentable does not have an available API, and Hacker Brunch uses a web scraper to look up available reservations on www.opentable.com for the next 4 weekends for groups of 2, 4 or 6 people.

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/homepage.png'>

Tech Stack
------
* Python, Javascript/jQuery, AJAX/JSON, Jinja, Flask, Bootstrap, HTML/CSS, Posgresql, SQLAlchemy
* APIs used: Yelp Search API, Google Maps JavaScript API, Twilio SMS

Features
------
* **_Restaurant List_** - Restaurants available on Hacker Brunch, with a link to the Yelp page of each, and information on neighborhood and cuisine
* **_Reservation List_** - Available Opentable reservations for the coming weekends; users can populate a Google Map to see markers for restaurants with reservation availability
* **_User Feedback on Restaurants_** - When a user is logged in, they have the option to save their feedback for each restaurant in the "Restaurant" page ('want to try', 'like', or 'dislike')
* **_User Notifications_** - When a user is logged in, they can set up notifications for restaurants that don't currently have available reservations so they can receive a text message as soon as a reservation for that restaurant, time and number of people is available

Screen Shots
------
**Restaurants**

All available restaurants on Hacker Brunch. Data is provided by the Yelp Search API. When a user is logged in, they have the ability to indicate whether they "want to try" a restaurant, or if they "like" or "dislike" a restaurant if they've been there in the past.

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/restaurants.png'>

**Reservations**

Available upcoming reservations for all restaurants featured on Hacker Brunch. For restaurants that don't currently have any available reservations, users have the option to sign-up for SMS text notifications (powered by Twilio) so they get a notification as soon as Hacker Brunch knows a reservation that matches the user's preferences becomes available.

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/reservations.png'>

**Google Map**

Users can filter restaurants based on number of people, date, and even by restaurant name. When a user clicks on "Populate Map," markers appear on the San Francisco map based on filters the user has selected.

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/googlemap.png'>

**Notifications**

List of all notifications for upcoming reservations that has been set up by the users. As soon as a text message is sent to the user, the notification is deleted from the database so the user only receives the reminder once. Users have the ability to cancel future notifications if needed.

<img src='https://github.com/tinapastelero/hacker-table/blob/master/static/notification.png'>

Author
------
Tina Pastelero is based in San Francisco, CA.
