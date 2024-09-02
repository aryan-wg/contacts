import unittest
from unittest.mock import patch,Mock
from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con

from src.entities.admin.admin import Admin  # Adjust import according to your project structure

patch.TEST_PREFIX = ('test','setUp')
# from src.utils.db_utils import (
#     read_fields_from_record,
#     update_one_record,
#     write_to_table,
#     check_if_exists_in_db
# )
# from src.utils.general_utils import (
#     parse_requests,
#     populate_requests,
#     hash_pass
# )

class TestAdmin(unittest.TestCase):
    def __init__(self):
        self.empId = 1
        self.name = "test case"
        self.phone = 998822331
        self.email = "aryan@email.com"
        self.address = "{\"street\": \"test street\", \"postal_code\": \"666666\", \"city\": \"Test_city\", \"state\": \"test_state\", \"country\": \"test_country\"}"
        self.employee_info = (self.empId,self.name,self.phone,self.email,self.address)
    
    @patch("Admin.get_pending_req")
    def setUp(self,mock_pending) -> None:
        mock_response = Mock()
        response_pending = []
        mock_response.return_value = response_pending
        mock_pending.return_value = mock_response

        self.admin_obj = Admin(self.employee_info)
        return super().setUp()

    def test_commit_request(self):
        print(self.admin_obj)
        # assert 
if __name__ == '__main__':
    unittest.main()
