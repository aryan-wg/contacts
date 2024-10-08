from ..employee.employee import Employee
from ...utils.db_utils import (
    read_fields_from_record,
    update_one_record,
    write_to_table,
    check_if_exists_in_db,
)
from ...utils.general_utils import  hash_pass
from ...utils.parsing_populating_utils import parse_requests, populate_requests

from math import ceil
import time

import json


class Admin(Employee):
    def __init__(self, employee_info):
        super().__init__((*employee_info, "admin"))

    def get_pending_req(self):
        # for a request to be pending it should have req_status == approved_by_hr
        data = read_fields_from_record(
            "requests", "*", "request_status", ["approved_by_hr"]
        )
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    def get_closed_req(self):
        # for a request to be closed it should have req_status == committed or rejected
        data = read_fields_from_record(
            "requests", "*", "request_status", ["committed", "rejected"]
        )
        print(data)
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    def commit_request(self, req_id):
        # get request information
        request = read_fields_from_record("requests", "*", "request_id", [req_id])
        request = parse_requests(request)
        request = request[0]

        # parse the json obj of update to updated dict
        updated_info = json.loads(request["updated_info"])

        # the address field has sub fields and should be stored as a stringified json obj
        updated_info["address"] = json.dumps(updated_info["address"])

        # update the employee record
        update_one_record("employees", updated_info, "empId", request["created_by"])

        # update the request status to committed and add commit time
        request["update_committed_at"] = ceil(time.time())
        request["request_status"] = "committed"
        update_one_record("requests", request, "request_id", req_id)
        return True

    def create_new_employee(self, new_employee):
        new_employee["password"] = hash_pass(new_employee["password"])
        created_employee = write_to_table("employees", new_employee)
        return created_employee

    def create_new_relation(self, emp_id, reports_to_emp_id):
        check = check_if_exists_in_db("employees", "empId", reports_to_emp_id)
        if not check:
            return False
        else:
            new_relation = {}
            new_relation["employee"] = emp_id
            new_relation["reports_to"] = reports_to_emp_id
            created_relation = write_to_table("relations", new_relation)
            return created_relation

    def info(self):
        doc = """
            This is the admin user class it has the following methods
            - Edit workers info
            - Add new worker
            - Remove worker
            - Approve a request
        """
        print(doc)
