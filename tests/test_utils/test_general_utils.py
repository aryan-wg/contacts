import unittest
from unittest.mock import Mock, patch,call
import io
from src.utils.general_utils import hash_pass,take_address_input


class Test_general_utils(unittest.TestCase):
    def setUp(self) -> None:
        self.message = "Enter an input"
        self.email = "test@test.com"
        self.phone = 934420830100
        self.password = "1@tEst78"
        self.address = {
                "street":"test_street",
                "postal_code":"247001",
                "city":"test_city",
                "state":"test_state",
                "country":"test_country"
        }
        self.hash = hash_pass(self.password)
        self.keys_for_printable = [
            "request_id",
            "created_by",
            "assigned_hr",
            "update_committed_at",
            "created_at",
        ]
        self.data_for_printable = [
            {
                "request_id": 3,
                "created_by": "dev",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": "shruti",
                "remark": None,
                "created_at": "2024-08-29 22:41:38",
                "update_committed_at": 0,
                "request_status": "rejected",
            }
        ]
        self.requests_to_parse = [
            (
                1,
                1,
                '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                2,
                None,
                1724941498,
                0,
                "approved_by_hr",
            )
        ]
        self.requests_to_populate = [
            {
                "request_id": 1,
                "created_by": 1,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": 2,
                "remark": None,
                "created_at": 1724941498,
                "update_committed_at": 0,
                "request_status": "approved_by_hr",
            }
        ]
        self.relations_to_parse = [
            (1, 3, "devs"),
            (2, 3, "devs"),
            (1, 3, "devs"),
            (2, 3, "devs"),
            (1, 3, "devs"),
            (2, 3, "devs"),
            (1, 3, "devs"),
            (2, 3, "devs"),
        ]
        self.relations_to_populate = [{"reports_to": 3, "empId": 7}]

        input_patcher = patch("builtins.input")
        self.mock_input = input_patcher.start()
        output_patcher = patch("builtins.print")
        self.mock_print = output_patcher.start()

    def test_int_input(self):
        self.mock_input.side_effect = ['should not work','12']
        
        res = int_input("test")
        assert res == 12
        self.mock_input.assert_called_with("test")

        self.mock_print.assert_called_once_with("Invalid input try again")

        # expected_calls = [call("Invalid input try again")]
        # self.mock_print.assert_has_calls(expected_calls) 

    def test_take_address_input(self):
        #arrang
        self.mock_input.side_effect = [self.address["street"],"123",self.address["postal_code"],self.address["city"],self.address["state"],self.address["country"]]

        #act
        address = take_address_input()
            
        #assert
        self.mock_print.assert_called_with("Enter a valid pin code \n")
        assert address == '{"street": "test_street", "postal_code": 247001, "city": "test_city", "state": "test_state", "country": "test_country"}' 

    def test_make_printable(self):
        pass


    # def test_hash_pass(self):
    #     # output_hash = hash_pass("test_password")
    #     #     
    #     # assert output_hash == '$2b$12$qg0xePyBWbkkgGHEe88fk.aabBlBdXpPpbtvA7CJQSPdB1K88xlnS'
    #     pass
    #
    # def test_check_pass(self):
    #     pass
