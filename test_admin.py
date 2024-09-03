import unittest
from unittest.mock import patch,Mock
from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con

from src.entities.admin.admin import Admin  # Adjust import according to your project structure

class TestAdmin(unittest.TestCase):

    @patch("test_admin.Admin.get_pending_req")
    @patch("test_admin.Admin.get_closed_req")
    def get_admin_obj(mock_get_closed_req, mock_get_pending_req):
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = "{\"street\": \"test street\", \"postal_code\": \"666666\", \"city\": \"Test_city\", \"state\": \"test_state\", \"country\": \"test_country\"}"
        employee_info = (empId, name, phone, email, address)
        mock_get_closed_req.return_value = 1
        mock_get_pending_req.return_value = 1
        return Admin(employee_info)
    
    def setUp(self) -> None:
        
        self.admin_obj = TestAdmin.get_admin_obj()
        print(f'REQ: {self.admin_obj.pending_req}')

    def test_commit_request(self):

        # assert 
if __name__ == '__main__':
    unittest.main()

