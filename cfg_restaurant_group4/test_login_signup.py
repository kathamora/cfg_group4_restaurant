from login_signup import get_signup_login_choice, login_signup_choice
import unittest
from unittest.mock import patch, MagicMock
import login_signup
from sql_connection import mydb

class TestShowSignup(unittest.TestCase):

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_signup_email_exists(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_email_exists.return_value = True
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_signup()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with("Email already exists")

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_signup_username_exists(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_email_exists.return_value = False
        authenticator_mock.check_username_exists.return_value = True
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_signup()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with("Username already exists")

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_signup_value_error(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_email_exists.side_effect = ValueError('Some error message')
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_signup()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with('Some error message')

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_signup_success(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_email_exists.return_value = False
        authenticator_mock.check_username_exists.return_value = False
        authenticator_mock.signup.return_value = ('username', 'password', 'email')
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_signup()

        self.assertEqual(result, ('username', 'password', 'email'))
        st_mock.success.assert_called_once_with("Account created successfully")
class TestShowLogin(unittest.TestCase):
    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_login_success(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_username_exists.return_value = True
        authenticator_mock.get_user_info.return_value = ('user_id', 'username', 'email', 'password')
        UserAuthenticatorMock.return_value = authenticator_mock

        with patch.object(login_signup.st, 'text_input') as text_input_mock:
            text_input_mock.side_effect = ['username', 'password']

            with patch.object(login_signup.st, 'button') as button_mock:
                button_mock.return_value = True

                result = login_signup.show_login()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'username')
        self.assertEqual(result[1], 'password')

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_login_username_not_exists(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_username_exists.return_value = False
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_login()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with("Username does not exist")

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_login_incorrect_password(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_username_exists.return_value = True
        authenticator_mock.get_user_info.return_value = ('user_id', 'username', 'email', 'wrong_password')
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_login()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with("Incorrect password")

    @patch('login_signup.UserAuthenticator')
    @patch('login_signup.st')
    def test_show_login_value_error(self, st_mock, UserAuthenticatorMock):
        authenticator_mock = MagicMock()
        authenticator_mock.check_username_exists.side_effect = ValueError('Some error message')
        UserAuthenticatorMock.return_value = authenticator_mock

        st_mock.button.return_value = True

        result = login_signup.show_login()

        self.assertIsNone(result)
        st_mock.error.assert_called_once_with('Some error message')

class TestUserAuthenticator(unittest.TestCase):

    @patch('login_signup.show_signup')
    def test_login_signup_choice_sign_up(self, mock_show_signup):
        mock_show_signup.return_value = ('username', 'password', 'email')
        result = login_signup_choice('Sign up')
        self.assertEqual(result, (None, None, None))

    @patch('login_signup.show_login')
    def test_login_signup_choice_login(self, mock_show_login):
        mock_show_login.return_value = ('username', 'password')
        result = login_signup_choice('Login')
        self.assertEqual(result, (None, None, None))

    def test_login_signup_choice_no_choice(self):
        result = login_signup_choice(mydb)
        self.assertEqual(result, (None, None, None))

    def test_get_signup_login_choice(self):
        with patch('login_signup.st.radio', return_value='Sign up'):
            result = get_signup_login_choice()
            self.assertEqual(result, 'Sign up')

        with patch('login_signup.st.radio', return_value='Login'):
            result = get_signup_login_choice()
            self.assertEqual(result, 'Login')

if __name__ == '__main__':
    unittest.main()



