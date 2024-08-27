from ..employee.employee import Employee
from ..worker.worker import Worker
from ..hr.hr_employee import Hr_employee
from ../../utils/utils.py import write_to_table

class Admin(Employee):
    def __init__(self, name, phone, email, address):
        self.pending_req = []
        self.closed_req = []

        super().__init__(name, phone, email, address)
        print("new admin initiated", self.name)

    def edit_worker_info(self, emp_id, updated):
        print(f"employee with employee id {emp_id} will be updated to", updated)
        raise NotImplemented("writing to database is not implemented yet")

    def create_worker(self, *args):
        # print(*args,"args for creating worker in the admin class")
        new_worker = Worker(*args)
        return new_worker

    def create_hr_emp(self, *args):
        # new_hr_emp = Hr_employee(*args)

        # this will require the following employee info:
        # {
        #     "employee_name":"string",
        #     "phone_no":"integer",
        #     "email":"string",
        #     "address":"json obj serialised",
        #     "password":"bcrypt hashed string",
        #     "user_type":"worker (string)",
        # }
        data_obj = {}
        write_to_table("employee",data_obj)
        return new_hr_emp

    def info(self):
        return """
            This is the admin user class it has the following methods
            - Edit workers info
            - Add new worker
            - Remove worker
            - Approve a request
        """
