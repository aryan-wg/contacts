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
                
                employee_info = (empId,name,phone,email,address)

                check = bcrypt.checkpw(password,hashed_db.encode())
                if check:
                    if user_type == "admin":
                        new_admin = Admin(employee_info)
                        return new_admin

                    elif user_type == "hr":
                        new_hr = Hr_employee(employee_info)
                        return new_hr

                    elif user_type == "worker":
                        new_worker = Worker(employee_info)
                        return new_worker

                else:
                    return None
        except NameError as err:
            pass
