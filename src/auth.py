import bcrypt

from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
from .utils.db_utils import read_fields_from_record
from .utils.general_utils import check_pass

class Auth:
    def __init__(self, empId, password):
        self.password = password
        self.empId = empId

    def login(self):
        try:
            user = read_fields_from_record("employees", "*", "empId", [self.empId])
            if user :
                # print(user)
                _,name,phone,email,address,hashed_db,user_type = user[0]
                
                employee_info = (self.empId,name,phone,email,address)

                check = check_pass(self.password,hashed_db)
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
