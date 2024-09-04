import unittest
from unittest.mock import patch, Mock

# from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con
from pprint import pprint
from src.entities.admin.admin import (
    Admin,
)  # Adjust import according to your project structure


class TestAdmin(unittest.TestCase):

    def setUp(self) -> None:
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666", "city": "Test_city", "state": "test_state", "country": "test_country"}'
        employee_info = (empId, name, phone, email, address)
        self.admin_obj = Admin(employee_info)

    # @patch("src.utils.general_utils.read_fields_from_record")
    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.utils.db_utils.read_fields_from_record")
    def test_get_pending_req(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = (
            [
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
            ],
        )
        mock_parse_req.return_value = (
            [
                {
                    "assigned_hr": 2,
                    "created_at": 1724941498,
                    "created_by": 1,
                    "remark": None,
                    "request_id": 1,
                    "request_status": "approved_by_hr",
                    "update_commited_at": 0,
                    "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                    '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                    'rd", "state": "uttar pradesh", "postal_code": 206301, '
                    '"country": "India"}}',
                }
            ],
        )
        mock_populate_req.return_value = [
            {
                "assigned_hr": "shruti",
                "created_at": "2024-08-29 19:54:58",
                "created_by": "Aryan",
                "remark": None,
                "request_id": 1,
                "request_status": "approved_by_hr",
                "update_commited_at": 0,
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                'rd", "state": "uttar pradesh", "postal_code": 206301, '
                '"country": "India"}}',
            }
        ]
        data = self.admin_obj.get_pending_req()
        assert data == [
            {
                "request_id": 1,
                "created_by": "Aryan",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": "shruti",
                "remark": None,
                "created_at": "2024-08-29 19:54:58",
                "update_commited_at": 0,
                "request_status": "approved_by_hr",
            }
        ]

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.utils.db_utils.read_fields_from_record")
    def test_get_pending_req_2(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = ([])
        mock_parse_req.return_value = ([])
        mock_populate_req.return_value = []
        data = self.admin_obj.get_pending_req()
        assert data == []

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.utils.db_utils.read_fields_from_record")
    def test_get_closed_req(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = (
            [
                (
                    1,
                    1,
                    '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                    2,
                    None,
                    1724941498,
                    1724942498,
                    "commited",
                )
            ],
        )
        mock_parse_req.return_value = (
            [
                {
                    "assigned_hr": 2,
                    "created_at": 1724941498,
                    "created_by": 1,
                    "remark": "test_remark",
                    "request_id": 1,
                    "request_status": "commited",
                    "update_commited_at": 1724942498,
                    "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                    '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                    'rd", "state": "uttar pradesh", "postal_code": 206301, '
                    '"country": "India"}}',
                }
            ],
        )
        mock_populate_req.return_value = [
            {
                "assigned_hr": "shruti",
                "created_at": "2024-08-29 19:54:58",
                "created_by": "Aryan",
                "remark": "test_remark",
                "request_id": 1,
                "request_status": "commited",
                "update_commited_at": "2024-08-29 20:11:38",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                'rd", "state": "uttar pradesh", "postal_code": 206301, '
                '"country": "India"}}',
            }
        ]
        data = self.admin_obj.get_pending_req()
        assert data == [
            {
                "request_id": 1,
                "created_by": "Aryan",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                "assigned_hr": "shruti",
                "remark": "test_remark",
                "created_at": "2024-08-29 19:54:58",
                "update_commited_at": "2024-08-29 20:11:38",
                "request_status": "commited",
            }
        ]

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.utils.db_utils.read_fields_from_record")
    def test_get_closed_req_2(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = ([])
        mock_parse_req.return_value = ([])
        mock_populate_req.return_value = []
        data = self.admin_obj.get_closed_req()
        assert data == []

    def test_commit_request(self):
        pass
    def test_create_new_employee(self):
        pass

    def test_create_new_relation(self):
        pass


if __name__ == "__main__":
    unittest.main()


# @patch("test_admin.Admin.get_pending_req")
# @patch("test_admin.Admin.get_closed_req")
# def get_admin_obj(mock_get_closed_req, mock_get_pending_req):
#     empId = 1
#     name = "test case"
#     phone = 998822331
#     email = "aryan@email.com"
#     address = "{\"street\": \"test street\", \"postal_code\": \"666666\", \"city\": \"Test_city\", \"state\": \"test_state\", \"country\": \"test_country\"}"
#     employee_info = (empId, name, phone, email, address)
#     mock_get_closed_req.return_value = 1
#     mock_get_pending_req.return_value = 1
#     return Admin(employee_info)
#
# def setUp(self) -> None:
#
#     self.admin_obj = TestAdmin.get_admin_obj()
#     print(f'REQ: {self.admin_obj.pending_req}')
