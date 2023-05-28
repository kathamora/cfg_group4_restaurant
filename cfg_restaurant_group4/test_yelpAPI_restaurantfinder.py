import unittest
from unittest.mock import patch
from api_final import RestaurantFinder, YelpAPI
from config import API_Key
import requests

#In this check, we bypassed the Streamlit commands as we want to check the functionality of the backend more.
# Checking YelpAPI class
class YelpAPITestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = API_Key
        self.yelp_api = YelpAPI(self.api_key)

    @patch('requests.get')
    def test_search_businesses_valid_connection(self, sample_get):
        # Create mock/invented response for the API, just to see if it connects or things get retrieved
        sample_response = {
            'businesses': [
                {
                    'name': 'Zuni',
                    'location': {
                        'city': 'London',
                        'display_address': ['Baker St.']
                    },
                    'rating': 4.0,
                    'price': '££',
                    'phone': '987654321',
                    'review_count': 75,
                    'categories': [{'title': 'Vietnamese'}],
                    'url': 'http://yelp.com/Zuni',
                }
            ]
        }

        # Create a mock response by mocking requests.get function and calling the json method
        sample_get.return_value.json.return_value = sample_response
        print(sample_response)
        # Simulate a successful response
        sample_get.return_value.status_code = 200

        # Test search_businesses function with "mock" details
        results = self.yelp_api.search_businesses('London', 'Vietnamese', '4.0')

        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Zuni')
        self.assertEqual(results[0]['city'], 'London')
        self.assertEqual(results[0]['address'], 'Baker St.')
        self.assertEqual(results[0]['rating'], 4.0)
        self.assertEqual(results[0]['price'], '££')
        self.assertEqual(results[0]['phone'], '987654321')
        self.assertEqual(results[0]['review_count'], 75)
        self.assertEqual(results[0]['cuisine'], ['Vietnamese'])
        self.assertEqual(results[0]['url'], 'http://yelp.com/Zuni')
        self.assertEqual(results[0]['is_favorite'], False)

        # Verify that the API was called with the correct parameters
        expected_params = {'term': 'Vietnamese', 'location': 'London', 'rating': '4.0'}
        expected_headers = {'Authorization': f'Bearer {self.api_key}'}
        # Check whether the API link with correct headers and parameters are called once
        sample_get.assert_called_once_with(
            'https://api.yelp.com/v3/businesses/search',
            headers=expected_headers,
            params=expected_params
        )

    @patch('requests.get')
    def test_search_businesses_invalid_connection(self, sample_get):
        # Trigger exception handling to be raised when connection fails
        sample_get.side_effect = requests.exceptions.RequestException('Invalid connection')

        # Create AssertRaise when a ValueError occurs
        with self.assertRaises(ValueError) as e:
            self.yelp_api.search_businesses('London', 'Vietnamese', '4.0')

        # Check the error message when ValueError happens
        self.assertEqual(str(e.exception), 'Please enter correct Location.')


# Checking RestaurantFinder class
class RestaurantFinderTestCase(unittest.TestCase):
    #Testing get_user_input function while mocking search_businesses
    def test_get_input_valid(self):
        api_key = API_Key
        username = "software1"
        restaurant_finder = RestaurantFinder(api_key, username)
        restaurant_finder.location = 'New York'
        restaurant_finder.cuisine = 'Italian'
        restaurant_finder.rating = 4.5

        # Mocking the search_businesses method to return a sample response
        sample_response = [
            {
                'name': 'Restaurant 1',
                'city': 'New York',
                'address': '123 Main St',
                'rating': 4.5,
                'price': '$$',
                'phone': '123-456-7890',
                'review_count': 100,
                'cuisine': ['Italian'],
                'url': 'https://restaurant1.com',
                'is_favorite': False
            }
        ]
        with patch.object(YelpAPI, 'search_businesses', return_value=sample_response):
            restaurant_finder.get_user_input()

        # Assert that the search results are populated with the sample response
        self.assertEqual(restaurant_finder.all_results, sample_response)

    def test_get_input_invalid(self):
        api_key = API_Key
        username = "software1"
        restaurant_finder = RestaurantFinder(api_key, username)
        restaurant_finder.location = ''
        restaurant_finder.cuisine = 'Invalid Cuisine'
        restaurant_finder.rating = 6.0

        # Mocking the search_businesses method to raise a ValueError
        with patch.object(YelpAPI, 'search_businesses', side_effect=ValueError("Invalid input")):
            restaurant_finder.get_user_input()

        # Assert that the error message is displayed
        # Check if search results are empty
        self.assertEqual(restaurant_finder.all_results, [])
        # Check if favorites are empty
        self.assertEqual(len(restaurant_finder.favorites), 0)
        # Check if search button is not clicked
        self.assertEqual(restaurant_finder.search_button, False)
        # Check if favorite button is not clicked
        self.assertEqual(restaurant_finder.favorite_button, False)

if __name__ == '__main__':
    unittest.main()


''' In the first part, I added to test whether there is a valid or invalid connection call to the API, thus I created
a class to test the YelpAPI function. 
First I created a setUp function (similar to __init__ in the original class) containing the keys and initiating the 
class YelpAPI call from the class_api_resto file
After that I called the @patch('requests.get') decorator to mock the request.get function. 
To test the search_business function with "sample get" as a parameter, I created a sample response mimicking a retrieved 
restaurant detail. I then created the "sample_response" dictionary as the result of mocking a call requests.get function 
and calling the json method
I also mock that the connectio went through ("200") as status code.
Then proceeded to call the search_business function and create assertions that should match the sample response. 
Lastly, I called the API using the parameters needed to succesfully call it.'''

''' In the second one, I mocked what if the connection fails, and it should return the error message Fed created on the 
original file'''

"""In this test, I create an instance of RestaurantFinder and set the location, cuisine, and rating.I then mock the search_businesses method of the YelpAPI class 
 to return a sample response. Then I call the get_user_input method  and assert that the all_results 
attribute is populated with the sample response."""

"""i am creating an instance of RestaurantFinder and set invalid values for location, cuisine, and rating. 
then i  mock the search_businesses method of the YelpAPI class to raise a ValueError with the message "Invalid input".
in the end I call the get_user_input method and assert that the search results are empty, favorites are empty,
  and the search button and favorite button are not clicked"""