import unittest
from src.utils.input_utils import phone_input,email_input,password_input

from unittest.mock import patch,Mock

class test_input_utlis(unittest.TestCase):
    def setUp(self):
        input_patcher = patch("builtins.input")
        self.mock_input = input_patcher.start()
        output_patcher = patch("builtins.print")
        self.mock_print = output_patcher.start()

    @patch("src.utils.input_utils.validate_phone")
    def test_phone_input(self,patched_validate_phone):
        self.mock_input.side_effect = ["12345678900","1234567890"] 
        patched_validate_phone.side_effect = [False,True]
        res = phone_input({"user_type":"hr"})
        self.mock_print.assert_called
        assert res["phone"] == '1234567890'

    @patch("src.utils.input_utils.validate_email")
    def test_email_input(self,patched_validate_email):
        patched_validate_email.side_effect = [False,True]
        self.mock_input.side_effect = ["test.email.com","test@test.com"] 
        res = email_input({"user_type":"hr"})

        self.mock_print.assert_called
        assert res["email"] == 'test@test.com'

    @patch("src.utils.input_utils.validate_password")
    def test_password_input(self,patched_validate_password):
        patched_validate_password.side_effect = [False,True]
        self.mock_input.side_effect = ["Test12","Test@123"] 
        res = password_input({"user_type":"hr"})

        self.mock_print.assert_called
        assert res["password"] == 'Test@123'
