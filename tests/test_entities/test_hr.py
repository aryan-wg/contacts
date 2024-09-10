import unittest
from unittest.mock import patch, Mock
from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con

from src.entities.hr.hr_employee import (
    Hr_employee,
)  # Adjust import according to your project structure


class TestHr(unittest.TestCase):
    def setUp(self) -> None:
        empId = 2
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666", "city": "Test_city", "state": "test_state", "country": "test_country"}'
        user_type = "hr"
        employee_info = (empId, name, phone, email, address)
        self.hr_obj = Hr_employee(employee_info)

    @patch("src.entities.hr.hr_employee.populate_requests")
    @patch("src.entities.hr.hr_employee.parse_requests")
    @patch("src.entities.hr.hr_employee.read_by_multiple_attributes")
    def test_get_pending_req(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = [
            (
                1,
                1,
                '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                2,
                None,
                1724941498,
                0,
                "hr_assigned",
            )
        ]
        mock_parse_req.return_value = [
            {
                "assigned_hr": 2,
                "created_at": 1724941498,
                "created_by": 1,
                "remark": None,
                "request_id": 1,
                "request_status": "hr_assigned",
                "update_committed_at": 0,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
            }
        ]
        mock_populate_req.return_value = [
            {
                "assigned_hr": "shruti",
                "created_at": "2024-08-29 19:54:58",
                "created_by": "Aryan",
                "remark": None,
                "request_id": 1,
                "request_status": "hr_assigned",
                "update_committed_at": 0,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
            }
        ]
        data = self.hr_obj.get_pending_requests()
        assert data == [
            {
                "request_id": 1,
                "created_by": "Aryan",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": "shruti",
                "remark": None,
                "created_at": "2024-08-29 19:54:58",
                "update_committed_at": 0,
                "request_status": "hr_assigned",
            }
        ]

    @patch("src.entities.hr.hr_employee.populate_requests")
    @patch("src.entities.hr.hr_employee.parse_requests")
    @patch("src.entities.hr.hr_employee.read_by_multiple_att_and_keys")
    def test_get_closed_req(self, mock_read_db_call, mock_parse_req, mock_populate_req):
        mock_read_db_call.return_value = [
            (
                1,
                1,
                '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                2,
                None,
                1724941498,
                0,
                "committed",
            )
        ]
        mock_parse_req.return_value = [
            {
                "assigned_hr": 2,
                "created_at": 1724941498,
                "created_by": 1,
                "remark": None,
                "request_id": 1,
                "request_status": "committed",
                "update_committed_at": 0,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
            }
        ]
        mock_populate_req.return_value = [
            {
                "assigned_hr": "shruti",
                "created_at": "2024-08-29 19:54:58",
                "created_by": "Aryan",
                "remark": None,
                "request_id": 1,
                "request_status": "committed",
                "update_committed_at": 0,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
            }
        ]
        data = self.hr_obj.get_closed_requests()
        mock_read_db_call.assert_called_with(
            "requests",
            "*",
            ["request_status", "assigned_hr"],
            [["committed", "rejected", "approved_by_hr"], 2],
        )
        assert data == [
            {
                "request_id": 1,
                "created_by": "Aryan",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": "shruti",
                "remark": None,
                "created_at": "2024-08-29 19:54:58",
                "update_committed_at": 0,
                "request_status": "committed",
            }
        ]

    @patch("src.entities.hr.hr_employee.update_one_record")
    @patch("src.entities.hr.hr_employee.read_fields_from_record")
    def test_update_request_status(self,mock_read_db_call,mock_update_record):
        mock_read_db_call.return_value = [
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
        request = 
        mock_update_record.assert_called_with("requests",request,"request_id",1)
    def test_reject_request(self):
        pass


if __name__ == "__main__":
    unittest.main()
