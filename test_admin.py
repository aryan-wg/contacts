import unittest
from unittest.mock import patch
import json
import time
from math import ceil
import sqlite3
from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con
from src.entities.admin.admin import Admin  # Adjust import according to your project structure
from src.utils.db_utils import (
    read_fields_from_record,
    update_one_record,
    write_to_table,
    check_if_exists_in_db
)
from src.utils.general_utils import (
    parse_requests,
    populate_requests,
    hash_pass
)
class AdminOld(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup database before all tests."""
        cls.conn = sqlite3.connect(":memory:")  # Use in-memory database for testing
        cls.cursor = cls.conn.cursor()
        create_tables()
        insert_sample_data()


    def setUp(self):
        self.worker_info = {"name": "John Doe", "empId": "123"}
        self.admin = Admin(self.worker_info)

    @patch('your_module.read_fields_from_record')
    @patch('your_module.parse_requests')
    @patch('your_module.populate_requests')
    def test_get_pending_req(self, mock_populate_requests, mock_parse_requests, mock_read_fields):
        mock_read_fields.return_value = [{'request_status': 'approved_by_hr'}]
        mock_parse_requests.return_value = [{'request_status': 'approved_by_hr'}]
        mock_populate_requests.return_value = [{'request_status': 'approved_by_hr'}]
        
        result = self.admin.get_pending_req()
        self.assertEqual(result, [{'request_status': 'approved_by_hr'}])
        mock_read_fields.assert_called_with("requests", "*", "request_status", ["approved_by_hr"])
        mock_parse_requests.assert_called_once()
        mock_populate_requests.assert_called_once()

    @patch('your_module.read_fields_from_record')
    @patch('your_module.parse_requests')
    @patch('your_module.populate_requests')
    def test_get_closed_req(self, mock_populate_requests, mock_parse_requests, mock_read_fields):
        mock_read_fields.return_value = [{'request_status': 'commited'}]
        mock_parse_requests.return_value = [{'request_status': 'commited'}]
        mock_populate_requests.return_value = [{'request_status': 'commited'}]
        
        result = self.admin.get_closed_req()
        self.assertEqual(result, [{'request_status': 'commited'}])
        mock_read_fields.assert_called_with("requests", "*", "request_status", ["commited", "rejected"])
        mock_parse_requests.assert_called_once()
        mock_populate_requests.assert_called_once()

    @patch('your_module.read_fields_from_record')
    @patch('your_module.update_one_record')
    @patch('your_module.json.loads')
    @patch('your_module.time.time', return_value=1234567890)
    def test_commit_request(self, mock_time, mock_json_loads, mock_update_one_record, mock_read_fields):
        # Mock request data
        mock_read_fields.return_value = [{'request_id': '1', 'created_by': 'emp_1', 'updated_info': '{"address": {"city": "Test"}}'}]
        mock_json_loads.return_value = {"address": {"city": "Test"}}
        
        # Call commit_request method
        result = self.admin.commit_request('1')
        
        # Assertions
        self.assertTrue(result)
        mock_read_fields.assert_called_with("requests", "*", "request_id", ['1'])
        mock_update_one_record.assert_any_call("employees", {'address': json.dumps({"city": "Test"}), 'created_by': 'emp_1'}, "empId", 'emp_1')
        mock_update_one_record.assert_any_call("requests", {'request_id': '1', 'created_by': 'emp_1', 'update_commited_at': 1234567890, 'request_status': 'commited'}, "request_id", '1')

    @patch('your_module.write_to_table')
    @patch('your_module.hash_pass')
    def test_create_new_employee(self, mock_hash_pass, mock_write_to_table):
        mock_hash_pass.return_value = b'hashed_password'
        mock_write_to_table.return_value = {"empId": "456"}
        new_employee = {"name": "Jane Doe", "password": "password"}
        
        result = self.admin.create_new_employee(new_employee)
        
        self.assertEqual(result, {"empId": "456"})
        mock_hash_pass.assert_called_with("password")
        mock_write_to_table.assert_called_with("employees", {"name": "Jane Doe", "password": "hashed_password"})

    @patch('your_module.write_to_table')
    @patch('your_module.check_if_exists_in_db')
    def test_create_new_relation(self, mock_check_if_exists, mock_write_to_table):
        mock_check_if_exists.return_value = True
        mock_write_to_table.return_value = {"relation_id": "789"}
        
        result = self.admin.create_new_relation("123", "456")
        
        self.assertEqual(result, {"relation_id": "789"})
        mock_check_if_exists.assert_called_with("employees", "empId", "456")
        mock_write_to_table.assert_called_with("relations", {"employee": "123", "reports_to": "456"})

    def test_info(self):
        expected_doc = """
            This is the admin user class it has the following methods
            - Edit workers info
            - Add new worker
            - Remove worker
            - Approve a request
        """
        self.assertEqual(self.admin.info(), expected_doc)

class TestAdmin(unittest.TestCase):
    empId = 1
    name = "test case"
    phone = 998822331
    email = "aryan@email.com"
    address = "{\"street\": \"test street\", \"postal_code\": \"666666\", \"city\": \"Test_city\", \"state\": \"test_state\", \"country\": \"test_country\"}"
    employee_info = (empId,name,phone,email,address)
    admin_obj = Admin(employee_info)
     
    def test_get_pending_req():
        assert 
if __name__ == '__main__':
    unittest.main()
