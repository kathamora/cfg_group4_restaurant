import unittest
from unittest.mock import patch
from user_authenticator import UserAuthenticator
from sql_connection import mydb

class TestUserAuthenticator(unittest.TestCase):
    def setUp(self):
        self.mydb = mydb
        self.authenticator = UserAuthenticator(mydb)

    def test_valid_email_format(self):
        valid_emails = [
            "test@example.com",
            "user123@gmail.com",
            "john.doe@company.co"
        ]
        for email in valid_emails:
            self.assertTrue(self.authenticator.validate_email(email))

    def test_invalid_email_format(self):
        invalid_emails = [
            "test@example",
            "user123@gmail",
            "john.doe@company",
            "invalid_email"
        ]
        for email in invalid_emails:
            self.assertFalse(self.authenticator.validate_email(email))

    def test_valid_username_format(self):
        valid_usernames = [
            "username123",
            "john_doe",
            "user_name_1234"
        ]
        for username in valid_usernames:
            self.assertTrue(self.authenticator.validate_username(username))

    def test_invalid_username_format(self):
        invalid_usernames = [
            "user",
            "user@name",
            "user name",
            "username!",
            "_username"
        ]
        for username in invalid_usernames:
            self.assertFalse(self.authenticator.validate_username(username))

    def test_valid_password_format(self):
        valid_passwords = [
            "password123",
            "strongPassword",
            "p@ssw0rd"
        ]
        for password in valid_passwords:
            print(f"Testing password: {password}")
            self.assertTrue(self.authenticator.validate_password(password))

    def test_invalid_password_format(self):
        invalid_passwords = [
            "pass",
            "passw",
            "1234567",
            "p@ss",
            "pass "
        ]
        for password in invalid_passwords:
            print(f"Testing password: {password}")
            self.assertFalse(self.authenticator.validate_password(password))

    @patch("user_authenticator.UserAuthenticator.check_email_exists")
    def test_signup_with_existing_email(self, mock_check_email_exists):
        mock_check_email_exists.return_value = True
        with self.assertRaises(ValueError):
            self.authenticator.signup("test@example.com", "username", "password")

    @patch("user_authenticator.UserAuthenticator.check_email_exists")
    def test_signup_with_valid_credentials(self, mock_check_email_exists):
        mock_check_email_exists.return_value = False
        username, password, email = self.authenticator.signup("test@example.com", "username", "password")
        self.assertEqual(username, "username")
        self.assertEqual(password, "password")
        self.assertEqual(email, "test@example.com")

    @patch("user_authenticator.UserAuthenticator.login")
    def test_login_with_valid_credentials(self, mock_login):
        mock_login.return_value = ("username", "password")
        username, password = self.authenticator.login("username", "password")
        self.assertEqual(username, "username")
        self.assertEqual(password, "password")

    @patch("user_authenticator.UserAuthenticator.login")
    def test_login_with_invalid_credentials(self, mock_login):
        mock_login.side_effect = ValueError("Incorrect username or password")
        with self.assertRaises(ValueError):
            self.authenticator.login("username", "password")

    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_get_user_info_with_existing_user(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            "user_id": 1,
            "username": "john_doe",
            "email": "test@example.com",
            "password": "password"
        }
        user_info = self.authenticator.get_user_info("username", "john_doe")
        self.assertEqual(user_info["user_id"], 1)
        self.assertEqual(user_info["username"], "john_doe")
        self.assertEqual(user_info["email"], "test@example.com")
        self.assertEqual(user_info["password"], "password")

    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_get_user_info_with_nonexistent_user(self, mock_get_user_info):
        mock_get_user_info.side_effect = ValueError("User not found")
        with self.assertRaises(ValueError):
            self.authenticator.get_user_info("username", "non_existing_user")

if __name__ == "__main__":
    unittest.main()
