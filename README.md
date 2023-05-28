### Final project document
This is the final project of the Group 4 of the Spring 2023 CFG Degree: Restaurant Recommender Hungry Hunter.

Thanks to all main contributors:

- Kathleen Kay Amora (Kath)
- Federica Cimino (Fed)
- Mungunzaya Ganbat (Munguu)
- Nia Jones (Nia)

### Application logic:
- User authentication: The app verifies the user's credentials with the SQL database (restaurant_app) and creates a session token for the user. If user credential does not exist in the database, it will automatically add it to the users table in database table through connecting Python to SQL.
- User credentials verification: The app also checks the user’s input, whether the username, email and passwords follow the correct format.
- User profile creation: The app saves the user's profile information in the SQL database.
- User filters and restaurant recommendation: The app sends an HTTP GET request to the Yelp Fusion API with the required parameters based on the user’s preferences  and henceforth retrieves a list of recommended restaurants. User sees the result  in a web page through Streamlit package.
- User favorites. Users can favorite a restaurant they like or would like to visit, and the results will then be saved to the SQL DB, restaurants table with restaurant_ID as the primary key and user_ID as a foreign key from the users table.
- User review and rating: Based on the favorite restaurants list, the  app saves the user's review and rating in the review table in the SQL database with review_ID as the primary key. Two foreign keys (restaurant_ID, user_ID) were successfully incorporated as well. 
- User favorites, review, rating display. After successfully adding favorites, reviews and rating, by visiting the My Favorites, Reviews and Rating tabs, the user can see all his comments and favorites from the creation of their accounts up until the recent one. The data has been imported from the restaurants and reviews table in the SQL database, and has been fetched given that the user_ID matches the current session’  username. 


### Non-technical requirements:
- Security: The User authentication feature enables us to verify user’s credentials. 
- Compatibility: The app’s minimum requirements in Windows 11 and Mac OS environment, with Python 3.10 or later installed in the computer. Streamlit packages as well as other modules stated in the above list (e.g. pymysql, mysql-connector) should be installed.
- Performance: The app is expected to load within 2 seconds
- Usability:  Due to the usage of Streamlit package, the user will have an ease using the app through the GUI in an web browser, providing a more user-friendly manner of navigation
- Documentation: This documentation provides a detailed and comprehensive report of the software development process and the key features of our system.

### Technical requirements: 
- When using the app, the following should be done:
- Make sure the computer has the minimum requirement stated in the Compatibility section above.
- User has to download all the folders in the project 
- User needs to ensure all the relevant libraries are installed by checking (for front-end: check environment.txt)
- Make sure to input your own SQL credentials in the config.py file before running. 
- Users need to create the database using SQL and create the users table using database.sql file.
- Make sure to install all packages/requirements listed above before running.
- To run GUI, type streamlit run home.py in the terminal.

### Tools and libraries

**Tools**

- Python 3.6 - 3.10
- PyCharm / VsCode
- mySQL