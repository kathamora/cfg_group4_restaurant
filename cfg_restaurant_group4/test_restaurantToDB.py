from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from api_final import RestaurantToDB


class TestRestaurantToDB(unittest.TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.user = 'test_user'
        self.password = 'test_password'
        self.database = 'test_database'
        self.restaurant = RestaurantToDB(self.host, self.user, self.password, self.database)

    def tearDown(self):
        pass

    def test_add_data_to_db_valid(self):                                                    #passed
        # Mock the create_connection method to return a mock connection object
        with patch('api_final.sql.connect') as mock_connect:
            mock_connection = mock_connect.return_value
            mock_cursor = mock_connection.cursor.return_value
            mock_cursor.fetchall.return_value = []  # Return an empty list to simulate no existing restaurants

            # Provide mock input for username and favorite_restaurants
            username = 'test_user'
            favorite_restaurants = [{'name': 'Restaurant A', 'city': 'City A', 'address': 'Address A', 'rating': 4.5,
                                     'price': '$$', 'phone': '123456789', 'review_count': 10,
                                     'cuisine': ['Italian', 'Pizza'], 'url': 'example.com', 'is_favorite': True}]

            self.restaurant.add_data_to_db(username, favorite_restaurants)

            # Assert that the appropriate SQL queries and executions were made
            mock_connect.assert_called_once_with(host=self.host, user=self.user, password=self.password,
                                                 database=self.database)
            mock_cursor.execute.assert_called_with('SELECT user_ID, name FROM restaurants')
            mock_cursor.executemany.assert_called_once()

    def test_add_data_to_db_invalid(self):                                           #passed
        # Mock the create_connection method to return a mock connection object
        with patch('api_final.sql.connect') as mock_connect:
            mock_connection = mock_connect.return_value
            mock_cursor = mock_connection.cursor.return_value
            mock_cursor.fetchall.return_value = []  # Return an empty list to simulate no existing restaurants

            # Provide mock input for username and favorite_restaurants
            username = 'test_user'
            favorite_restaurants = [{'name': 'Restaurant A', 'city': 'City A', 'address': 'Address A', 'rating': 4.5,
                                     'price': '$$', 'phone': 'abcdef', 'review_count': 10,
                                     'cuisine': ['Italian', 'Pizza'], 'url': 'example.com', 'is_favorite': True}]

            try:
                self.restaurant.add_data_to_db(username, favorite_restaurants)
                # If the code reaches this point, the test should fail because an AssertionError was expected.
                raise AssertionError("Phone number must be numerical values only.")
            except AssertionError:
                # The AssertionError was raised as expected, so the test passes.
                pass

            # Assert that the appropriate SQL queries and executions were made
            mock_connect.assert_called_once_with(host=self.host, user=self.user, password=self.password,
                                                 database=self.database)
            mock_cursor.execute.assert_called_with('SELECT user_ID, name FROM restaurants')
            mock_cursor.executemany.assert_called_once()

    def test_save_review_rating_to_db(self):
        # Mock the create_connection method to return a mock connection object
        with patch('api_final.sql.connect') as mock_connect:
            mock_connection = mock_connect.return_value
            mock_cursor = mock_connection.cursor.return_value
            mock_cursor.fetchone.return_value = [1]  # Return a user_id and restaurant_id



            # Define the input parameters
            username = 'test_user'
            restaurant = 'Restaurant A'
            review = 'Great food and service!'
            rating = 4.5

            # Call the save_review_rating_to_db method
            self.restaurant.save_review_rating_to_db(username, restaurant, review, rating)

            # Assert the expected method calls and parameter values
            mock_connect.assert_called_once_with(host=self.restaurant.host, user=self.restaurant.user,
                                                 password=self.restaurant.password, database=self.restaurant.database)
            mock_cursor.execute.assert_any_call('SELECT User_ID FROM users WHERE Username = %s', username)
            mock_cursor.execute.assert_any_call('SELECT restaurant_ID FROM restaurants WHERE name = %s', restaurant)
            mock_cursor.execute.assert_called_with(
                'INSERT INTO reviews (user_ID, restaurant_ID, name, review, rating, timestamp) VALUES (%s, %s, %s, %s, %s, %s)',
                (1, 1, 'Restaurant A', 'Great food and service!', 4.5, datetime(2023, 5, 28, 20, 0, 13, 126157)))

            # Assert that the connection was committed and closed
            mock_connection.commit.assert_called_once()
            mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
