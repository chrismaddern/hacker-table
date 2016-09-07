import unittest
 
from server import app
from model import *
from datetime import datetime
from scraper import *


class HackerBrunchTests(unittest.TestCase):
    """Hacker Brunch tests"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = 'tina@gmail.com'

        # # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb")

        # # Create tables and add sample data
        # db.create_all()
        # example_data()

    # # Done at the end of each test
    # def tearDown(self):
    #     db.session.close()
    #     db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Hacker Brunch", result.data)

    def test_reservations(self):
        result = self.client.get("/reservations")
        self.assertIn("Available Reservation Times", result.data)

    def test_restaurants(self):
        result = self.client.get("/restaurant_list")
        self.assertIn("Neighborhood", result.data)

    def test_user(self):
        result = self.client.get("/user")
        self.assertIn("Your existing notifications", result.data)

    def test_create(self):
        result = self.client.post("/create",
                                  data={'user_email': 'tina@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn("brunch reservations", result.data)

    def test_notify(self):
        result = self.client.post("/notify",
                                  data={'user_id': 1, 'opentable': 1234, 'date': 'Sep10', 'people': 2, 'mobile': 123456},
                                  follow_redirects=True)
        self.assertIn("Available Reservation Times", result.data)

    def test_login(self):
        result = self.client.post("/login",
                                  data={'user_email': 'tina@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn("brunch reservations", result.data)

    def test_logout(self):
        self.client.post("/logout", follow_redirects=True)

    def test_cancel(self):
        result = self.client.post("/cancel", data={'user_id': 1, 'opentable': 1234, 'date': datetime(2016, 9, 10, 0, 0), 'people': 2},
                                  follow_redirects=True)
        self.assertIn("Your existing notifications", result.data)

    def test_update_status(self):
        result = self.client.post("/update_status", data={'user_id': 1, 'id': 1, 'status': 'try'})
        self.assertIn("try", result.data)

    def test_update_status2(self):
        result = self.client.post("/update_status", data={'user_id': 1, 'id': 1, 'status': 'like'})
        self.assertIn("like", result.data)

    def test_resto_markers(self):
        result = self.client.post("/resto_markers", data={'date': "", 'resto': "", 'people': ""})
        self.assertIn("1300", result.data)

    def test_resto_markers2(self):
        result = self.client.post("/resto_markers", data={'date': "Sep 9, Fri", 'resto': "", 'people': ""})
        self.assertIn("1300", result.data)


class HackerBrunchTestsLogout(unittest.TestCase):
    """Hacker Brunch tests"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     # Done at the end of each test
#     def tearDown(self):
#         db.session.close()
#         db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Hacker Brunch", result.data)

    def test_reservations(self):
        result = self.client.get("/reservations")
        self.assertIn("Available Reservation Times", result.data)

    def test_restaurants(self):
        result = self.client.get("/restaurant_list")
        self.assertIn("Neighborhood", result.data)
        self.assertNotIn("Want to Try", result.data)

    def test_logout(self):
        self.client.post("/logout", follow_redirects=True)

if __name__ == "__main__":
    unittest.main()
