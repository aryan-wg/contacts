from ...utils.general_utils import parse_requests,populate_requests
from ..worker.worker import Worker
from ...utils.db_utils import update_one_record,read_fields_from_record,read_by_multiple_attributes,read_by_multiple_att_and_keys
from math import ceil
import json
from pprint import pprint

class Hr_employee(Worker):
    def __init__(self,employee_info):

        # print("these are the args",employee_info)
        super().__init__(employee_info)
        
        self.type = "hr"
        # self.pending_req = self.get_pending_requests()
        # self.closed_req = self.get_closed_requests()

    def get_pending_requests(self):
        # all of the requests that have a status == hr_assigned and assigned_hr == self.empId are pending_requests
        data = read_by_multiple_attributes("requests","*",["request_status","assigned_hr"],["hr_assigned",self.empId]) 
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        # pprint(data)
        return data

    def get_closed_requests(self):
        # all of the requests that have a status == commited or rejected and assigned_hr = self.empId are closed requests 
        data = read_by_multiple_att_and_keys("requests","*",["request_status","assigned_hr"],[["commited","rejected","approved_by_hr"],self.empId])
        if data:
            data = parse_requests(data)
            data = populate_requests(data)
        # pprint(data)
        return data

    def update_request_status(self,req_id, remark,status):
        request = read_fields_from_record("requests","*","request_id",[req_id])
        request = parse_requests(request)
        request = request[0]
        # request has a possible value of none which can cause error here 

        request["remark"] = remark        
        request["request_status"] = "approved_by_hr" if status == "approve" else "rejected"    
        
        # update the request status to commited and add commit time 
        update_one_record("requests",request,"request_id",req_id)
        return True

    def reject_request(self,requestId, remark):
        print(f"request with {requestId} id is rejected with remark {remark}")
        raise NotImplementedError("Database setup for reject request is not implemented yet")

    def save(self):
        print("Saving the hr employee info to db")

# print("hr_employee.py")
