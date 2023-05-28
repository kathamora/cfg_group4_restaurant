import streamlit as st
import requests
from datetime import datetime
import pymysql as sql
from config import HOST, USER, PASSWORD

class YelpAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_businesses(self, location, cuisine, rating):
        """Retrieves necessary information for the API based on user's input of location, cuisine, and rating"""
        try:
            if not location or not cuisine or not rating:
                raise ValueError("Please enter all the required inputs.")

            params = {'term': cuisine, 'location': location, 'rating': rating}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            response = requests.get('https://api.yelp.com/v3/businesses/search', headers=headers, params=params)
            response.raise_for_status()  # Raise an exception if the request was not successful
            data = response.json()

            if 'error' in data:
                error_message = data['error']['description']
                raise ValueError(f"An error occurred: {error_message}")

            results = []
            for business in data.get('businesses', []):
                categories = [category['title'] for category in business.get('categories', [])]
                if cuisine.lower() in [cat.lower() for cat in categories] and business.get('rating', 0) == float(
                        rating):
                    details = {
                        'name': business['name'],
                        'city': business['location']['city'],
                        'address': ', '.join(business['location']['display_address']),
                        'rating': business.get('rating', 'N/A'),
                        'price': business.get('price', 'N/A'),
                        'phone': business.get('phone', 'N/A'),
                        'review_count': business.get('review_count', 'N/A'),
                        'cuisine': categories,
                        'url': business.get('url', 'N/A'),
                        'is_favorite': False
                    }
                    results.append(details)

            return results

        except ValueError as e:
            raise ValueError(str(e))
        except requests.exceptions.RequestException:
            raise ValueError("Please enter correct Location.")


class RestaurantFinder:
    def __init__(self, api_key, username):
        self.api_key = api_key
        self.yelp_api = YelpAPI(api_key)
        self.location = ''
        self.cuisine = ''
        self.rating = 0.0
        self.favorite_restaurants = []
        self.search_button = False
        self.all_results = []
        self.favorites = []
        self.favorite_button = False
        self.restaurant_to_DB = RestaurantToDB(HOST, USER, PASSWORD, database="restaurant_app")
        self.username = username
    def main(self):
        st.markdown("<h1 style='text-align: center;'>Restaurant Finder</h1>", unsafe_allow_html=True)
        """ Main website page on Streamlit"""
        with st.sidebar:
            st.header("Search Restaurants:")
            # Get user input
            self.get_user_input()
        # Update is_favorite for all search results based on user input
        self.all_results_with_fav = self.update_is_favorite(self.all_results, self.favorites, self.favorite_restaurants)
        # Show search results
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            self.show_search_results()
        # Show favorites
        with col2:
            self.show_favorites()
        # Show review and rating
        with col3:
            self.show_review_rating()

    def show_review_rating(self):
        """Shows the review text box and rating slider so user can add their own review and rating"""
        # Create multiselect dropdown for favorited restaurants only
        st.markdown("<h3 style='text-align: center;'> Add Your Own Review/Rating </h3>", unsafe_allow_html=True)
        selected_names = [result['name'] for result in self.favorite_restaurants]
        selected_restaurants = st.multiselect('Select ONE Restaurant', selected_names)

        if selected_restaurants:
            for restaurant in selected_restaurants:
                st.write(f"Restaurant: {restaurant}")
                review = self.add_review()
                rating = self.add_rating()

                col1, col2 = st.columns(2)
                if col1.button('Submit'):
                    self.restaurant_to_DB.save_review_rating_to_db(self.username, restaurant, review, rating)
                    st.success('Review/Rating submitted successfully!')
                if col2.button('Cancel'):
                    review = ""
                    rating = ""
                    st.warning('Review/Rating submission cancelled.')
                    break

        else:
            st.warning('Please select at least one restaurant')

    def get_user_input(self):
        """Function that is responsible for getting and storing the input from the user so includes text boxes and multiselect"""

        self.location = st.text_input('Location e.g., London', ' ').strip()
        self.cuisine = st.text_input('Cuisine e.g., Mexican, Korean', ' ').strip()
        self.rating = st.number_input('Rating (e.g. 3.5)', min_value=0.0, max_value=5.0, step=0.5)
        self.favorite_restaurants = st.session_state.get('favorites', [])
        self.search_button = st.button('Search')
        try:
            self.all_results = self.yelp_api.search_businesses(self.location, self.cuisine, self.rating)
            if not self.all_results:
                raise ValueError("No restaurants found for the given cuisine. Please try a different cuisine.")
        except ValueError as e:
            st.error(str(e))  # Display the error message to the user
            self.all_results = []  # Set an empty list for the search results
        except requests.exceptions.RequestException as e:
            st.error("An error occurred while making the API request. Please try again later.")
            self.all_results = []  # Set an empty list for the search results
        st.header("Choose your favorites:")
        restaurant_names = [result['name'] for result in self.all_results]
        selected_names = [result['name'] for result in self.favorite_restaurants]
        options = [name for name in restaurant_names if name not in selected_names]
        self.favorites = st.multiselect('Select favorite restaurants', options)
        self.favorite_button = st.button('Show Favorites')

    def update_is_favorite(self, all_results, favorites, favorite_restaurants):
        """Function that adds restaurants with is_favorite set to true to favorite restaurants and returns all_result
        with updated is_favorite in all_results"""
        for result in all_results:
            is_favorite = result['name'] in favorites
            result['is_favorite'] = is_favorite
            if is_favorite and result not in favorite_restaurants:
                favorite_restaurants.append(result)
            elif not is_favorite and result in favorite_restaurants:
                favorite_restaurants.remove(result)
        st.session_state.favorites = favorite_restaurants
        return all_results

    def show_search_results(self):
        """ Function that shows the search results in the Streamlit web app"""
        st.markdown("<h3 style='text-align: center;'>List of Restaurants </h3>", unsafe_allow_html=True)
        if self.search_button:
            st.subheader(f'Search results for {self.cuisine} with {self.rating} rating in {self.location}:')
            if len(self.all_results_with_fav) > 0:
                for result in self.all_results_with_fav:
                    st.write(f"Name:  {result['name']}  \n"
                             f"City:  {result['city']}  \n"
                             f"Address: {result['address']}  \n"
                             f" Rating:  {result['rating']}  \n"
                             f"Price:  {result['price']}   \n"
                             f"Phone:   {result['phone']}  \n"
                             f"Review Count:  {result['review_count']}  \n"
                             f"Cuisine: {', '.join(result['cuisine'])}  \n")
                    url = result['url']
                    if url != 'N/A':
                        st.markdown(f'<a href="{url}" target="_blank">Website Link</a>', unsafe_allow_html=True)
                    st.write('---')

    def show_favorites(self):
        """ Function that shows the favorites list in the Streamlit web app"""
        st.markdown("<h3 style='text-align: center;'> Favorites </h3>", unsafe_allow_html=True)
        if self.favorite_button:
            if len(self.favorite_restaurants) == 0:
                st.write('No favorites yet.')
            else:
                for favorite in self.favorite_restaurants:
                    st.write(f"Name: {favorite['name']}   \n"
                             f"City: {favorite['city']}   \n"
                             f"Address: {favorite['address']}  \n"
                             f"Rating: {favorite['rating']}  \n"
                             f"Price: {favorite['price']}  \n"
                             f"Phone: {favorite['phone']}  \n"
                             f"Review Count: {favorite['review_count']}  \n"
                             f"Cuisine: {', '.join(favorite['cuisine'])}  \n")
                    url = favorite['url']
                    if url != 'N/A':
                        st.markdown(f'<a href="{url}" target="_blank">Website Link</a>', unsafe_allow_html=True)
                    st.write('---')
            self.restaurant_to_DB.add_data_to_db(self.username, self.favorite_restaurants)



    def add_review(self):
        """ Add text box for review in Streamlit web interface"""
        review = st.text_area('Enter your review')
        return review

    # Function to add a rating
    def add_rating(self):
        """ Add slider from 1 to 5 in Streamlit web interface"""
        rating = st.slider('Rate the restaurant', 1, 5)
        return rating

    def run(self):
        """Method to run the Streamlit web app"""
        print("-------------New run, code updated-----------------")
        self.main()


class RestaurantToDB:
    def __init__(self, HOST, USER, PASSWORD, database='restaurant_app'):
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database = database

    def create_connection(self):
        connection = sql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        return connection

    def add_data_to_db(self, username, favorite_restaurants):
        ''' Put details on the favorites in the SQL table'''
        try:
            # Create connection to the MySQL database
            connection = self.create_connection()
            cursor = connection.cursor()

            # Get the user_ID from users table based on username
            query = '''SELECT User_ID FROM users WHERE Username = %s '''
            values = username
            print(username)
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            print(user_id)

            # Create the table in Python if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS restaurants (
                    restaurant_ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    user_ID INT NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    city VARCHAR(50) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    rating FLOAT,
                    price VARCHAR(20),
                    phone VARCHAR(50),
                    review_count INT,
                    cuisine VARCHAR(50),
                    url VARCHAR(255),
                    is_favorite BOOLEAN,
                    FOREIGN KEY (user_ID) REFERENCES users(User_ID)
                )
            ''')

            # Check if the user and restaurant combination is unique
            existing_user_restaurants = set()

            cursor.execute('SELECT user_ID, name FROM restaurants')
            for row in cursor.fetchall():
                existing_user_id = row[0]
                restaurant_name = row[1]

                existing_user_restaurants.add((existing_user_id, restaurant_name))

            # Convert to tuple so the pymysql can read it!
            new_restaurants = []
            for restaurant in favorite_restaurants:
                restaurant_name = restaurant['name']
                user_id_restaurant = (user_id, restaurant_name)
                if user_id_restaurant not in existing_user_restaurants:
                    cuisine = ', '.join(restaurant['cuisine'])  # Join cuisine list into a single string
                    values = (
                        user_id, restaurant['name'], restaurant['city'], restaurant['address'], restaurant['rating'],
                        restaurant['price'], restaurant['phone'], restaurant['review_count'],
                        cuisine, restaurant['url'], restaurant['is_favorite']
                    )
                    new_restaurants.append(values)
                    # unique_restaurants.append(restaurant['name'])

            # Insert new restaurants using executemany() so it is a BLOCK kind of listing
            print(new_restaurants)
            if new_restaurants:
                query = '''
                    INSERT INTO restaurants (user_id, name, city, address, rating, price, phone, review_count, cuisine, url, is_favorite)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.executemany(query, new_restaurants)

            # Commit and close connection
            connection.commit()
            connection.close()

            # Print message based on the number of restaurants added to the database
            num_restaurants = len(new_restaurants)
            print(
                f'{num_restaurants} new restaurant/s added to the database.' if num_restaurants > 0 else 'No new restaurants added.'
            )
        except sql.Error as e:
            print(f"An error occurred while adding data to the database: {str(e)}")


    def save_review_rating_to_db(self, username, restaurant, review, rating):
        """Save review and rating to a SQL database"""
        try:
            # Connect to the MySQL database
            connection = self.create_connection()
            cursor = connection.cursor()

            # Get the user_ID from users table based on username
            query = """SELECT User_ID FROM users WHERE Username = %s"""
            values = username
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            print(user_id)

            # Get the restaurant_ID from restaurants table based on name
            query = """SELECT restaurant_ID FROM restaurants WHERE name = %s"""
            values = restaurant
            cursor.execute(query, values)
            restaurant_id = cursor.fetchone()[0]

            # Create the table in Python if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    review_ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                    user_ID INT NOT NULL,
                    restaurant_ID INT NOT NULL,
                    name VARCHAR(50),
                    review TEXT,
                    rating FLOAT,
                    timestamp DATETIME,
                    FOREIGN KEY (restaurant_ID) REFERENCES restaurants(restaurant_ID),
                    FOREIGN KEY (user_ID) REFERENCES users(User_ID)
                )
            """)
            #Add this later once you can retrieve username/userID: FOREIGN KEY (user_ID) REFERENCES users(user_ID),
            # Insert the review, rating and timestamp details into the table
            query = """INSERT INTO reviews (user_ID, restaurant_ID, name, review, rating, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (user_id, restaurant_id, restaurant, review, rating, datetime.now())
            cursor.execute(query, values)

            # Execute commit and close connection
            connection.commit()
            connection.close()

            print("Review and rating saved to the database.")
        except sql.Error as e:
            print(f"An error occurred while saving review and rating to the database: {str(e)}")


    def display_restaurants(self, username):
        try:
            # Connect to the MySQL database
            connection = self.create_connection()
            cursor = connection.cursor()

            # Get the user_ID from users table based on username
            query = '''
                    SELECT User_ID FROM users WHERE Username = %s
                                '''
            values = username
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            # user_id = 1 # just to see if my database will show up in here with default 1

            # Update the SQL query to include the user ID filter
            query = "SELECT * FROM restaurants WHERE user_ID = %s"
            values = user_id
            cursor.execute(query, values)

            # Fetch all rows from the result
            restaurants = cursor.fetchall()

            # Display the data in Streamlit
            st.header("My Favorite Restaurants:")
            if len(restaurants) > 0:
                for restaurant in restaurants:
                    st.write(f"Name: {restaurant[2]}   \n"
                             f"City: {restaurant[3]}   \n"
                             f"Address: {restaurant[4]}  \n"
                             f"Rating: {restaurant[5]}  \n"
                             f"Price: {restaurant[6]}  \n"
                             f"Phone: {restaurant[7]}  \n"
                             f"Review Count: {restaurant[8]}  \n"
                             f"Cuisine: {', '.join(restaurant[9].split(', '))}  \n")
            else:
                st.write('No favorite restaurants yet.')
            # Close the connection
            cursor.close()
            connection.close()
            print("Restaurant details displayed in Streamlit page")
        except sql.Error as e:
            print(f"An error occurred while saving review and rating to the database: {str(e)}")

    def display_review_rating(self, username):
        try:
            connection = self.create_connection()
            cursor = connection.cursor()

            # Get the user_ID from users table based on username
            query = """SELECT User_ID FROM users WHERE Username = %s"""
            values = username
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            # user_id = 1

            # Update the SQL query to include the user ID filter
            query = "SELECT * FROM reviews WHERE user_ID = %s"
            values = user_id
            cursor.execute(query, values)

            # Fetch all rows from the result
            reviews = cursor.fetchall()

            # Display the data in Streamlit
            st.header("Review and Ratings:")
            if len(reviews) > 0:
                for entry in reviews:
                    st.write(f"Restaurant's Name: {entry[3]}   \n"
                             f"Review: {entry[4]}   \n"
                             f"Rating: {entry[5]}   \n"
                             f"Date and Time: {entry[6]}   \n")
            else:
                st.write('No reviews/ratings yet.')
            # Close the connection
            cursor.close()
            connection.close()
            print("Review and Rating details displayed in Streamlit page")
        except sql.Error as e:
            print(f"An error occurred while saving review and rating to the database: {str(e)}")

# if __name__ == '__main__':
#     st.set_page_config(page_title='Restaurant Finder', layout="wide")

#     api_key = API_Key
#     restaurant_finder = RestaurantFinder(api_key)
#     restaurant_finder.run()
