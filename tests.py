import unittest

from server import app
from model import db, connect_to_db

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///restaurants"


class HackerBrunchTests(unittest.TestCase):
    """Hacker Brunch tests"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app)

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = 'tina@gmail.com'

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Hacker Brunch", result.data)

    def test_login(self):
        result = self.client.post("/login",
                                  data={'user_email': 'tina@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn("brunch reservations", result.data)

    def test_logout(self):
        self.client.post("/logout", follow_redirects=True)

    def test_create(self):
        result = self.client.post("/create",
                                  data={'user_email': 'tina@gmail.com', 'password': 'password'},
                                  follow_redirects=True)
        self.assertIn("brunch reservations", result.data)

    def test_reservations(self):
        result = self.client.get("/reservations")
        self.assertIn("Available Reservation Times", result.data)

    def test_restaurants(self):
        result = self.client.get("/restaurant_list")
        self.assertIn("Neighborhood", result.data)

    def test_user(self):
        result = self.client.get("/user")
        self.assertIn("Your existing notifications", result.data)


class HackerBrunchDatabase(unittest.TestCase):
    """Database tests"""

	# Done at the start of each test
    def setup(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_email'] = 'tina@gmail.com'

	# Done at the end of each test
    def tearDown(self):
	    db.session.close()
	    db.drop_all()

if __name__ == "__main__":
    unittest.main()
