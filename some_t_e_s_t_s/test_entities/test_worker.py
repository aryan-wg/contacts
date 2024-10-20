import unittest
from unittest.mock import patch,Mock

from src.entities.worker.worker import Worker

class TestWorker(unittest.TestCase):
    def setUp(self) -> None:
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666", "city": "Test_city", "state": "test_state", "country": "test_country"}'
        user_type = "worker"
        employee_info = (empId, name, phone, email, address,user_type)
        self.worker_obj= Worker(employee_info)
    
    def test_reports_to(self):
        pass

    def test_reported_by(self):
        pass

if __name__ == "__main__":
    unittest.main() 
