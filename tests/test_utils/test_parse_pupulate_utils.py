import unittest
from unittest.mock import Mock, patch
from pprint import pprint
from src.utils.parsing_populating_utils import (
    parse_requests,
    parse_relations,
    populate_requests,
    populate_relations,
)


class Test_parse_populate_utils(unittest.TestCase):
    def test_parse_request(self):
        test_requests = [
            (0, 0, "updated_info_string", 0, None, 1725818219, 0, "hr_assigned")
        ]
        res = parse_requests(test_requests)
        assert res == [
            {
                "request_id": 0,
                "created_by": 0,
                "updated_info": "updated_info_string",
                "assigned_hr": 0,
                "remark": None,
                "created_at": 1725818219,
                "update_committed_at": 0,
                "request_status": "hr_assigned",
            }
        ]

    @patch("src.utils.parsing_populating_utils.read_fields_from_record")
    def test_populate_requests(self, mocked_db_req):
        mocked_db_req.side_effect = [(("created_by_emp",), ("assigned_hr_emp",)),(("created_by_emp",), ("assigned_hr_emp",))]
        parsed_requests = [
            {
                "request_id": 0,
                "created_by": 0,
                "updated_info": "updated_info_string",
                "assigned_hr": 0,
                "remark": None,
                "created_at": 1725818219,
                "update_committed_at": 0,
                "request_status": "hr_assigned",
            },
            {
                "request_id": 0,
                "created_by": 0,
                "updated_info": "updated_info_string",
                "assigned_hr": 0,
                "remark": None,
                "created_at": 1725818219,
                "update_committed_at": 1725818219,
                "request_status": "hr_assigned",
            }
        ]
        res = populate_requests(parsed_requests)
        assert res == [
            {
                "request_id": 0,
                "created_by": "created_by_emp",
                "updated_info": "updated_info_string",
                "assigned_hr": "assigned_hr_emp",
                "remark": None,
                "created_at": "2024-09-08 23:26:59",
                "update_committed_at": 0,
                "request_status": "hr_assigned",
            },
            {
                'assigned_hr': 'assigned_hr_emp',
                'created_at': '2024-09-08 23:26:59',
                'created_by': 'created_by_emp',
                'remark': None,
                'request_id': 0,
                'request_status': 'hr_assigned',
                'update_committed_at': '2024-09-08 23:26:59',
                'updated_info': 'updated_info_string',
            },
        ]

    def test_parse_relation(self):
        test_relations = [(0, 1)]
        res = parse_relations(test_relations)
        assert res == [
            {
                "reports_to": 0,
                "empId": 1,
            }
        ]

    @patch("src.utils.parsing_populating_utils.read_fields_from_record")
    def test_populate_relation(self, mocked_db_req):
        mocked_db_req.side_effect = [
                [("top_emp", "top_emp@test.com", "0000000000")],
                [("senior_name_test", "senior_email@test.com", "1234567890")],
                [("emp_name_test", "emp_email@test.com", "2222222222")],
        ]
        parsed_relations = [
            {
                "reports_to": 0,
                "empId": 1,
            },
            {
                "reports_to": 1,
                "empId": 2,
            },
        ]
        res = populate_relations(parsed_relations)
        pprint(res)
        assert res == [
            {
                "empId": 1,
                "reports_to": {
                    "name": None,
                    "email": None,
                    "phone": None,
                    "empId": None,
                },
                "employee": {
                    "name": "top_emp",
                    "email": "top_emp@test.com",
                    "phone": "0000000000",
                    "empId": 1,
                },
            },
            {
                "empId": 2,
                "reports_to": {
                    "name": "senior_name_test",
                    "email": "senior_email@test.com",
                    "phone": "1234567890",
                    "empId": 1,
                },
                "employee": {
                    "name": "emp_name_test",
                    "email": "emp_email@test.com",
                    "phone": "2222222222",
                    "empId": 2,
                },
            },
        ]
