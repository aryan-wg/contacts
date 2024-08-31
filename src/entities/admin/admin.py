from ..employee.employee import Employee
from ..worker.worker import Worker
from ..hr.hr_employee import Hr_employee
from ...utils.db_utils import read_fields_from_record, update_one_record, write_to_table
from ...utils.general_utils import parse_requests,populate_requests,hash_pass

from math import ceil
import time
from pprint import pprint

import json  
class Admin(Employee):
    def __init__(self, worker_info ):
        self.pending_req = self.get_pending_req()
        self.closed_req = self.get_closed_req()
        self.type = "admin"
        super().__init__(worker_info)
        # print("new admin initiated", self.name)

    def get_pending_req(self):
        # for a request to be pending it should have req_status == approved_by_hr
        data = read_fields_from_record(
            "requests", "*", "request_status", ["approved_by_hr"]
        )
        if data :
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    def get_closed_req(self):
        # for a request to be closed it should have req_status == commited
        data = read_fields_from_record(
            "requests", "*", "request_status", ["commited", "rejected"]
        )
        # print("somethin")
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        return data

    def commit_request(self, req_id):
        # get requst information 
        request = read_fields_from_record("requests","*","request_id",[req_id])
        request = parse_requests(request)
        request = request[0]

        # parse the json obj of update to updated dict
        updated_info = json.loads(request["updated_info"])
        
        # the address field has sub fields and should be stored as a stringified json obj
        updated_info["address"] = json.dumps(updated_info["address"])

        # update the employee record 
        update_one_record("employees",updated_info,"empId",request["created_by"])
        
        # update the request status to commited and add commit time 
        request["update_commited_at"] = ceil(time.time())
        request['request_status'] = "commited"
        # print(request)
        update_one_record("requests",request,"request_id",req_id)
        return True

    def create_new_worker(self,new_worker):
        new_worker["password"] = hash_pass(new_worker["password"])
        new_worker["user_type"] = "worker"
        print(new_worker)
        write_to_table("employees",new_worker)
        return True

        # print(*args,"args for creating worker in the admin class")
        # new_worker = Worker(*args)
        return new_worker

    def create_hr_emp(self, *args):
        pass
        # new_hr_emp = Hr_employee(*args)

        # this will require the following employee info:

        # data_obj = {
        #     "employee_name":"string",
        #     "phone_no":"integer",
        #     "email":"string",
        #     "address":"json obj serialised",
        #     "password":"bcrypt hashed string",
        #     "user_type":"worker (string)",
        # }

        # write_to_table ("employees",data_obj)
        # data_obj = 1
        # new_hr_emp = None
        # return new_hr_emp

    def info(self):
        doc = """
            This is the admin user class it has the following methods
            - Edit workers info
            - Add new worker
            - Remove worker
            - Approve a request
        """
        return doc
