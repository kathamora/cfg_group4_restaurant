import unittest
from unittest.mock import patch
from food_preferences import create_preferences


class TestCreatePreferences(unittest.TestCase):

    @patch('streamlit.multiselect')
    @patch('streamlit.button')
    @patch('food_preferences.mydb.cursor')
    def test_save_preferences_valid(self, mock_cursor, mock_button, mock_multiselect):
        mock_button.return_value = True
        mock_multiselect.side_effect = [['Vegetarian', 'Vegan'], ['Lactose intolerance', 'Diabetic']]
        with patch('streamlit.success') as mock_success:
            create_preferences('username')
            mock_cursor.return_value.execute.assert_called_once_with(
                "UPDATE users SET Food_preferences = %s, Dietary_requirements = %s WHERE Username = %s",
                ('Vegetarian,Vegan', 'Lactose intolerance,Diabetic', 'username'))
            mock_success.assert_called_once_with("Preferences saved successfully!")

    @patch('streamlit.multiselect')
    @patch('streamlit.button')
    def test_save_preferences_no_save(self, mock_button, mock_multiselect):
        mock_button.return_value = False
        with patch('streamlit.success') as mock_success, \
             patch('food_preferences.mydb.cursor') as mock_cursor:
            create_preferences('username')
            mock_cursor.assert_not_called()
            mock_success.assert_not_called()


if __name__ == '__main__':
    unittest.main()



