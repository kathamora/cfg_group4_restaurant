import streamlit as st
from sql_connection import mydb, DbConnectionError

def create_preferences(username):
    try:
        st.title(f"Welcome {username}!")
        st.header("Food Preferences")
        st.write("Please tell us more about your preferences")
        food_preferences = st.multiselect("Food preferences", ["Vegetarian", "Vegan", "Gluten-free", "Kosher", "Halal"])
        dietary_requirements = st.multiselect("Dietary restrictions", ["None", "Nut allergies", "Lactose intolerance", "Diabetic"])
        save_button = st.button("Save")

        if save_button:
            # Join the preferences and restrictions into a comma-separated string
            food_preferences_str = ",".join(food_preferences)
            dietary_restrictions_str = ",".join(dietary_requirements)

            # Update the values in the SQL table
            cursor = mydb.cursor()
            cursor.execute("UPDATE users SET food_preferences = %s, dietary_requirements = %s WHERE username = %s",
                           (food_preferences_str, dietary_restrictions_str, username))
            mydb.commit()
            st.success("Preferences saved successfully!")
            cursor.close()
            mydb.close()
    except DbConnectionError as error:
        st.error(f"Failed to save preferences: {error}")



