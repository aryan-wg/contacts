from ...utils.general_utils import parse_requests
from ..worker.worker import Worker
from ...utils.db_utils import read_by_multiple_attributes,read_by_multiple_att_and_keys
from pprint import pprint

class Hr_employee(Worker):
    def __init__(self,employee_info):

        print("these are the args",employee_info)
        super().__init__(employee_info)
        
        self.type = "hr"
        self.pending_requests = self.get_pending_requests()
        self.closed_requests = self.get_closed_requests()

    def get_pending_requests(self):
        # all of the requests that have a status == hr_assigned and assigned_hr == self.empId are pending_requests
        data = read_by_multiple_attributes("requests","*",["request_status","assigned_hr"],["hr_assigned",self.empId]) 
        data = parse_requests(data)
        # pprint(data)
        return data

    def get_closed_requests(self):
        # all of the requests that have a status == commited or rejected and assigned_hr = self.empId are closed requests 
        data = read_by_multiple_att_and_keys("requests","*",["request_status","assigned_hr"],[["commited","rejected","approved_by_hr"],self.empId])
        data = parse_requests(data)
        # pprint(data)
        return data

    def approve_request(self,requestId, remark):
        print(f"request with {requestId} id is approved with remark {remark}")
        raise NotImplementedError(
            "Database setup for approve request is not implemented yet"
        )

    def reject_request(self,requestId, remark):
        print(f"request with {requestId} id is rejected with remark {remark}")
        raise NotImplementedError("Database setup for reject request is not implemented yet")

    def save(self):
        print("Saving the hr employee info to db")

# print("hr_employee.py")
