import unittest
from unittest.mock import patch, Mock
from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con

from src.entities.hr.hr_employee import (
    Hr_employee,
)  # Adjust import according to your project structure


class TestHr(unittest.TestCase):
    def setUp(self) -> None:
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666", "city": "Test_city", "state": "test_state", "country": "test_country"}'
        user_type = "hr"
        employee_info = (empId, name, phone, email, address, user_type)
        self.hr_obj = Hr_employee(employee_info)

    def test_get_pending_req(self):
        pass

    def test_get_closed_req(self):
        pass

    def test_update_request_status(self):
        pass

    def test_reject_request(self):
        pass


if __name__ == "__main__":
    unittest.main()
