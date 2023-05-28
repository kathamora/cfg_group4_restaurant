import unittest
from unittest.mock import patch, MagicMock
from security import login_security_page

class TestLoginSecurityPage(unittest.TestCase):
    @patch('security.st')
    @patch('security.mydb')
    def test_email_change_success(self, mock_mydb, mock_st):
        # Mocking user input and session state
        mock_st.text_input.return_value = 'new_email'
        mock_st.button.return_value = True

        # Mocking database cursor and query execution
        mock_cursor = MagicMock()
        mock_mydb.cursor.return_value = mock_cursor

        # Calling the function under test
        login_security_page('test_user')

        # Asserting the success message is displayed
        mock_st.success.assert_called_with("Email updated successfully!")

if __name__ == '__main__':
    unittest.main()




