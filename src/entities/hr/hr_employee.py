from ..worker.worker import Worker


class Hr_employee(Worker):
    def __init__(self, *args):
        print(args)

        worker_information = args

        self.pending_requests = []
        self.closed_requests = []

        super().__init__(*worker_information)

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
