from ...utils.parsing_populating_utils import parse_requests, populate_requests
from ..worker.worker import Worker
from ...utils.async_pg_db_utils import (
    update_one_record,
    read_fields_from_record,
    read_by_multiple_attributes,
    read_by_multiple_att_and_keys,
    check_if_exists_in_db,
)
from math import ceil
import json
from pprint import pprint


class Hr_employee(Worker):
    def __init__(self, emp_id,logger):
        super().__init__(emp_id,logger)

    def get_pending_requests(self):
        # all of the requests that have a status == hr_assigned and assigned_hr == self.empId are pending_requests
        data = read_by_multiple_attributes(
            "requests",
            "*",
            ["request_status", "assigned_hr"],
            ["hr_assigned", self.emp_id],
        )
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    def get_closed_requests(self):
        # all of the requests that have a status == committed or rejected and assigned_hr = self.empId are closed requests
        data = read_by_multiple_att_and_keys(
            "requests",
            "*",
            ["request_status", "assigned_hr"],
            [["committed", "rejected", "approved_by_hr"], self.emp_id],
        )
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    async def get_assigned_requests_by_status(self, query_status_list):
        data = await read_by_multiple_att_and_keys(
            "requests",
            "*",
            ["request_status", "assigned_hr"],
            [query_status_list, self.emp_id],
        )
        if data:
            data = parse_requests(data)
            data = await populate_requests(data)
        return data

    async def update_request_status_with_remark(self, req_id, remark, status):
        if not await check_if_exists_in_db("requests", "request_id", req_id):
            raise ValueError("Request id does not exsists")
        else:
            request = await read_fields_from_record(
                "requests", "*", "request_id", [req_id]
            )
            request = parse_requests(request)
            request = request[0]
            # request has a possible value of none which can cause error here
            if not request["assigned_hr"] == self.emp_id:
                raise ValueError("Request is assigned to different hr")
            else:
                request["remark"] = remark
                if request["request_status"] == "hr_assigned":
                    request["request_status"] = status
                    request["updated_info"] = json.dumps(request["updated_info"])
                else:
                    ValueError("Request already reviewed by HR")

            await update_one_record("requests", request, "request_id", req_id)
            return True
