from ..worker.worker import Worker
class Hr_employee(Worker):
    def __init__(self,*args):
        print(args)

        pending_requests,closed_requests,worker_information = args

        self.pending_requests = pending_requests 
        self.closed_requests = closed_requests

        super().__init__(*worker_information)
    
    def approve_request(requestId,remark):
        print(f"request with {requestId} id is approved with remark {remark}")
        raise NotImplemented("Database setup for approve request is not implemented yet")
    def reject_request(requestId,remark):
        print(f"request with {requestId} id is rejected with remark {remark}")
        raise NotImplemented("Database setup for reject request is not implemented yet")
 
print("hr_employee.py")
