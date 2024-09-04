import unittest
from unittest.mock import Mock, patch

from src.utils.general_utils import hash_pass


class Test_general_utils(unittest.TestCase):
    def setUp(self) -> None:
        self.message = "Enter an input"
        self.email = "test@test.com"
        self.phone = 934420830100
        self.pin = 247001
        self.password = "1@tEst78"
        self.hash = hash_pass(self.password)
        self.keys_for_printable = [
            "request_id",
            "created_by",
            "assigned_hr",
            "update_commited_at",
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
                "update_commited_at": 0,
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
                "update_commited_at": 0,
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
        self.relations_to_pupulate = [{"reports_to": 3, "empId": 7}]

    def test_int_input(self):
        pass

    def test_take_address_input(self):
        pass

    def test_validate_email(self):
        pass

    def test_validate_phone(self):
        pass

    def test_validate_pin_code(self):
        pass

    def test_validate_password(self):
        pass

    def test_hash_pass(self):
        pass

    def test_check_pass(self):
        pass

    def test_make_printable(self):
        pass

    def test_parse_request(self):
        pass

    def test_populate_requests(self):
        pass

    def test_parse_relation(self):
        pass

    def test_populate_relation(self):
        pass
