import streamlit as st
st.set_page_config(page_title="Restaurant Finder", page_icon=":fork_and_knife:", layout="wide")
from login_signup import login_signup_choice,mydb, get_signup_login_choice
from security import login_security_page
from food_preferences import create_preferences
from delete_account import delete_my_account
from config import API_Key, HOST, USER, PASSWORD
from api_final import RestaurantFinder, RestaurantToDB


@st.cache_resource
class SessionState:
    def __init__(self):
        self.current_page = 0
        self.logged_in = False


state = SessionState()

if state.current_page == 0:
    st.title("Welcome to our Restaurant Recommender, 'Hungry Hunter'")
    st.markdown('Our service is to recommend you the best restaurant based on your interests')
    if not state.logged_in:
        choice = get_signup_login_choice()
        username, password, email = login_signup_choice(mydb, choice)
        if username and password:
            state.logged_in = True
            state.current_page += 1


if state.current_page == 1:
    if state.logged_in:
        username, password, email = login_signup_choice(mydb)
        st.sidebar.title(f"Hello {username}!")
        menu = ["About", "Food Preferences", "Restaurant Search", "My Favorites, Reviews and Ratings", "Login and Security", "Log out", "Delete my account"]
        sidebar_selection = st.sidebar.selectbox("Select a page", menu, key="sidebar_selectbox")

        if sidebar_selection == "About":
            st.markdown("<h2>About</h2>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-size: 18px; line-height: 1.5;'>Welcome to the Restaurant Finder app!</p>"
                "<p style='font-size: 18px; line-height: 1.5;'>Explore and discover restaurants based on your preferences.</p>"
                "<p style='font-size: 18px; line-height: 1.5;'>Navigate through different sections to manage your food preferences, search for restaurants, view your favorites, write reviews and ratings, and manage your account settings.</p>"
                "<p style='font-size: 18px; line-height: 1.5;'>Check the selection box on your left to get started!</p>"
                "<p style='font-size: 18px; line-height: 1.5;'>Enjoy and have fun!</p>",
                unsafe_allow_html=True
            )

        elif sidebar_selection == "Food Preferences":
            create_preferences(username=username)

        elif sidebar_selection == "Login and Security":
            login_security_page(username)
        # this one needs proper look at with sql

        elif sidebar_selection == "Restaurant Search":
            api_key = API_Key
            restaurant_finder = RestaurantFinder(api_key, username=username)
            restaurant_finder.run()

        elif sidebar_selection == "My Favorites, Reviews and Ratings":
            view_favorites_ratings = RestaurantToDB(HOST, USER, PASSWORD)
            col1, col2= st.columns([3, 3])
            with col1:
                view_favorites_ratings.display_restaurants(username)
            with col2:
                view_favorites_ratings.display_review_rating(username)

        elif sidebar_selection == "Log out":
            st.success("You have been logged out!")
            state.logged_in = False
            state.current_page = 0

        elif sidebar_selection == "Delete my account":
            delete_my_account(username)
            state.logged_in = False
            state.current_page = 0


