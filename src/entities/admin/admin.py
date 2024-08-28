from ..employee.employee import Employee
from ..worker.worker import Worker
from ..hr.hr_employee import Hr_employee
from ...utils.db_utils import read_fields_from_record, write_to_table
from ...utils.general_utils import parse_requests

class Admin(Employee):
    def __init__(self, empId, name, phone, email, address):
        self.pending_req = self.get_pending_req()
        self.closed_req = self.get_closed_req()

        super().__init__(empId, name, phone, email, address)
        # print("new admin initiated", self.name)

    def get_pending_req(self):
        # for a request to be pending it should have req_status == approved_by_hr
        data = read_fields_from_record(
            "requests", "*", "request_status", ["approved_by_hr"]
        )
        data = parse_requests(data)
        return data

    def get_closed_req(self):
        # for a request to be closed it should have req_status == commited
        data = read_fields_from_record(
            "requests", "*", "request_status", ["commited", "rejected"]
        )
        data = parse_requests(data)
        return data

    def edit_worker_info(self, emp_id, updated):
        print(f"employee with employee id {emp_id} will be updated to", updated)
        raise NotImplemented("writing to database is not implemented yet")

    def create_worker(self, *args):
        # print(*args,"args for creating worker in the admin class")
        new_worker = Worker(*args)
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
