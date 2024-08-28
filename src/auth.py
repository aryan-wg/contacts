import bcrypt

from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
# from .utils.utils import read_fields_from_record
from .utils.db_utils import read_fields_from_record


class Auth:
    def __init__(self, empId, password):
        self.password = password
        self.empId = empId

    def hash_pass(self):
        pass

    def login(self):
        password = self.password.encode()
        empId = self.empId
        try:
            user = read_fields_from_record("employees", "*", "empId", [empId])
            if user :
                _,name,phone,email,address,hashed_db,user_type = user[0]

                check = bcrypt.checkpw(password,hashed_db.encode())
                if check:
                    if user_type == "admin":
                        # empId, name, phone, email, address
                        new_admin = Admin(empId,name,phone,email,address)
                        return new_admin

                    # elif user_type == "hr":
                    #     # pending_requests = []
                    #     # closed_requests = []
                    #
                    #     new_hr = Hr_employee()
                    #     pass
                    # elif user_type == "worker":
                    #     # name, phone, email, address, empId = args
                    #
                    #     new_worker = Worker()
                    #     pass
                else:
                    return None
        except NameError as err:
            pass
