import unittest
from unittest.mock import patch, Mock, call

# from src.database.db_setup import create_tables, insert_sample_data, get_cursor, get_con

# from pprint import pprint
from src.entities.admin.admin import Admin


class TestAdmin(unittest.TestCase):
    def setUp(self) -> None:
        empId = 1
        name = "test case"
        phone = 998822331
        email = "aryan@email.com"
        address = '{"street": "test street", "postal_code": "666666", "city": "Test_city", "state": "test_state", "country": "test_country"}'
        self.employee_info = (empId, name, phone, email, address)
        self.new_emp_info = {
            "user_type":"hr",
            "name":"employee name",
            "phone":"1234567890",
            "email":"test@test.com",
            "address":'"{\\"street\\": \\"22\\", \\"postal_code\\": 234567, \\"city\\": \\"noida\\", \\"state\\": \\"up\\", \\"country\\": \\"ind\\"}"',
            "password":"unhased password"
        }
        self.parsed_req_dict = {
            "assigned_hr": 2,
            "created_at": 1724941498,
            "created_by": 1,
            "remark": "test_remark",
            "request_id": 1,
            "request_status": "committed",
            "update_committed_at": 1724942498,
            "updated_info": '{"name": "Akamboj", "phone": 12394823790,"email":"aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301,"country": "India"}}',
        }
        self.created_emp = (
            1,
            "employee name",
            1234567890,
            "test@test.com",
            '"{\\"street\\": \\"22\\", \\"postal_code\\": 234567, \\"city\\": \\"noida\\", \\"state\\": \\"up\\", \\"country\\": \\"ind\\"}"',
            "lets assume this is a hash",
            "hr",
        )
        self.admin_obj = Admin(self.employee_info)

    # @patch("src.utils.general_utils.read_fields_from_record")
    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.entities.admin.admin.read_fields_from_record")
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
                    "update_committed_at": 0,
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
                "update_committed_at": 0,
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
                "update_committed_at": 0,
                "request_status": "approved_by_hr",
            }
        ]

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.entities.admin.admin.read_fields_from_record")
    def test_get_pending_req_2(
        self, mock_read_fields, mock_parse_req, mock_populate_req
    ):
        mock_read_fields.return_value = []
        mock_parse_req.return_value = []
        mock_populate_req.return_value = []
        data = self.admin_obj.get_pending_req()
        assert data == []

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.entities.admin.admin.read_fields_from_record")
    def test_get_closed_req(self, mock_read_fields, mock_parse_req, mock_populate_req):
        mock_read_fields.return_value = [
            (
                1,
                1,
                '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                2,
                None,
                1724941498,
                1724942498,
                "committed",
            )
        ]

        mock_parse_req.return_value = (
            [
                {
                    "assigned_hr": 2,
                    "created_at": 1724941498,
                    "created_by": 1,
                    "remark": "test_remark",
                    "request_id": 1,
                    "request_status": "committed",
                    "update_committed_at": 1724942498,
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
                "request_status": "committed",
                "update_committed_at": "2024-08-29 20:11:38",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                'rd", "state": "uttar pradesh", "postal_code": 206301, '
                '"country": "India"}}',
            }
        ]
        data = self.admin_obj.get_pending_req()
        assert data == [
            {
                "assigned_hr": "shruti",
                "created_at": "2024-08-29 19:54:58",
                "created_by": "Aryan",
                "remark": "test_remark",
                "request_id": 1,
                "request_status": "committed",
                "update_committed_at": "2024-08-29 20:11:38",
                "updated_info": '{"name": "Akamboj", "phone": 12394823790, "email": '
                '"aryan@wg.com", "address": {"city": "noida", "street": "dl '
                'rd", "state": "uttar pradesh", "postal_code": 206301, '
                '"country": "India"}}',
            }
        ]

    @patch("src.entities.admin.admin.populate_requests")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.entities.admin.admin.read_fields_from_record")
    def test_get_closed_req_2(
        self, mock_read_fields, mock_parse_req, mock_populate_req
    ):
        mock_read_fields.return_value = []
        mock_parse_req.return_value = []
        mock_populate_req.return_value = []
        data = self.admin_obj.get_closed_req()
        assert data == []

    @patch("src.entities.admin.admin.update_one_record")
    @patch("src.entities.admin.admin.parse_requests")
    @patch("src.entities.admin.admin.read_fields_from_record")
    def test_commit_request(self, mock_read_db, mock_parse_req, mock_update_db):
        mock_read_db.return_value = [
            (
                1,
                1,
                '{"name": "Akamboj", "phone": 12394823790, "email": "aryan@wg.com", "address": {"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}}',
                2,
                None,
                1724941498,
                1724942498,
                "committed",
            )
        ]
        mock_parse_req.return_value = [self.parsed_req_dict]

        updated_info = {
            "name": "Akamboj",
            "phone": 12394823790,
            "email": "aryan@wg.com",
            "address": '{"city": "noida", "street": "dl rd", "state": "uttar pradesh", "postal_code": 206301, "country": "India"}',
        }
        self.admin_obj.commit_request(1)
        calls = [
            call("employees", updated_info, "empId", 1),
            call(
                "requests",
                self.parsed_req_dict,
                "request_id",
                1,
            ),
        ]
        mock_update_db.assert_has_calls(calls)
        pass

    @patch("src.entities.admin.admin.write_to_table")
    @patch("src.entities.admin.admin.hash_pass")
    def test_create_new_employee(self, mock_hash_pass, mock_write_to_db):
        mock_hash_pass.return_value = "lets assume this is a hash"
        mock_write_to_db.return_value = self.created_emp
        res = self.admin_obj.create_new_employee(self.new_emp_info)
        assert res == self.created_emp

    @patch("src.entities.admin.admin.check_if_exists_in_db")
    def test_create_new_relation(self,mock_check_db):
        mock_check_db.side_effect = [False,True]

        # will get false for the mock
        res1 = self.admin_obj.create_new_relation(2,7)

        # will get true for the mock
        res2 = self.admin_obj.create_new_relation(2,7)
        
        assert res1 is False
        assert res2 == (7,2)
    
    def test_info_fn(self):
        self.admin_obj.info()

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
