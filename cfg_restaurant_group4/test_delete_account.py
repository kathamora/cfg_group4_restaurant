import unittest
from unittest.mock import patch
from delete_account import delete_my_account, DbConnectionError


class TestDeleteAccount(unittest.TestCase):
    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_valid_account_deletion(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            "user_id": 1,
            "username": "john_doe"
        }
        delete_my_account("john_doe")

    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_db_connection_error(self, mock_get_user_info):
        mock_get_user_info.side_effect = DbConnectionError()
        delete_my_account("john_doe")


    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_account_deletion_with_special_characters(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            "user_id": 2,
            "username": "@user123"
        }
        delete_my_account("@user123")


    @patch("user_authenticator.UserAuthenticator.get_user_info")
    def test_account_deletion_already_deleted(self, mock_get_user_info):
        mock_get_user_info.return_value = {
            "user_id": 3,
            "username": "deleted_user"
        }
        delete_my_account("deleted_user")


if __name__ == "__main__":
    unittest.main()










