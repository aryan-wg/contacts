import unittest
from unittest.mock import Mock, patch

from src.entities.worker.worker import Worker


# employee class is an abstract class derived class instance needed to test it using worker
class test_employee(unittest.TestCase):
    def setUp(self) -> None:
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666","city": "Test_city", "state": "test_state", "country": "test_country"}'
        user_type = "hr"
        employee_info = (empId, name, phone, email, address, user_type)
        self.employee_obj = Worker(employee_info)

    def test_get_profile_info(self):
        pass

    def test_search_other_employee(self):
        pass

    def test_update_password(self):
        pass

    def test_request_self_info_change(self):
        pass


if __name__ == "__main__":
    unittest.main()
