import unittest
from unittest.mock import patch, MagicMock
import smtplib
from send_email import send_email

class SendEmailTestCase(unittest.TestCase):
    @patch('send_email.ssl.create_default_context')
    @patch('send_email.smtplib.SMTP_SSL')
    def test_send_email_valid(self, mock_smtp_ssl, mock_create_context):
        message = "Hello, World!"
        mock_context = MagicMock()
        mock_smtp = MagicMock()
        mock_create_context.return_value = mock_context
        mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp
        send_email(message)
        mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465, context=mock_context)
        mock_smtp.login.assert_called_once_with("cfgprojectqueries@gmail.com", "vknzegbybldhicxf")
        mock_smtp.sendmail.assert_called_once_with(
            "cfgprojectqueries@gmail.com", "cfgprojectqueries@gmail.com", message
        )

    @patch('smtplib.SMTP_SSL')
    def test_send_email_invalid(self, mock_smtp):
        message = "Hello, World!"
        with self.assertRaises(smtplib.SMTPException):
            mock_smtp.side_effect = smtplib.SMTPException("An error occurred")
            send_email(message)

    @patch('smtplib.SMTP_SSL')
    def test_send_email_edge_cases(self, mock_smtp):
        message = "Hello, World!"
        send_email(message)
        self.assertEqual(mock_smtp.call_count, 1)
        self.assertEqual(mock_smtp.return_value.login.call_count, 0)
        self.assertEqual(mock_smtp.return_value.sendmail.call_count, 0)

if __name__ == '__main__':
    unittest.main()

