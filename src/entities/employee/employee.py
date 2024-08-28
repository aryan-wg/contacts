from abc import ABC, abstractmethod
from time import time
from math import ceil


class Employee(ABC):
    def __init__(self, *args):
        empId,name, phone, email, address = args

        self.name = name
        self.phone = phone
        self.email = email
        self.empId = empId
        # this address will be a dict that has information
        # street,city,state,postal code, country

        self.address = address
        # print("new employee instantiated ", self.name)
        # print(self.name,self.phone,self.email,self.address)

    def search_other_employee(name):
        print("searchin for", name)

    def request_self_info_change(updated_info):
        # created_by integer NOT NULL, updated_info text NOT NULL, hr_assigned integer, approved_by_hr integer NOT NULL, remark text, created_at integer NOT NULL, update_commited integer NOT NULL
        request = {
            "created_by": self.empId,
            "updated_name": updated_info,
            "approved_by_hr": 0,
            "created_at": ceil(time.time()),
            "update_commited":0
        }

        print("updated user will be ", updated_user)

    def save(self):
        print("Saving the employee info to db")

    @abstractmethod
    def info():
        pass


# print("employee")

# name = "aryan"
# phone = "984783723"
# email = "aryan@gmail.com"
# address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}
# new_emp = employee(name,phone,email,address)
