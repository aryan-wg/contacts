from abc import abstractmethod,ABC 
import json
import time

from ...utils.general_utils import check_pass, hash_pass
from ...utils.db_utils import match_string_in_field, read_fields_from_record, update_one_record, write_to_table
from math import ceil
import random
class Employee(ABC):
    def __init__(self, employee_info):
        empId,name, phone, email, json_str_address,user_type = employee_info 
        # print(json_str_address)
        self.name = name
        self.phone = phone
        self.email = email
        self.empId = empId
        # this address will be a dict that has information
        # street,city,state,postal code, country
        parsed_address = json.loads(json_str_address)
        self.address = parsed_address
        self.user_type = user_type
        # print("new employee instantiated ", self.name)
        # print(self.name,self.phone,self.email,self.address)

    def get_profile_info(self):
        profile = {"name":self.name,"phone":self.phone,"email":self.email,"empId":self.empId,"address":self.address}
        return profile

    def search_other_employee(self,name):
        data = match_string_in_field("employees","empId, name, phone, email","name",name)  
        return data
    
    def update_password(self,old_pass,new_pass):
        hashed_pass = read_fields_from_record("employees", "password", "empId", [self.empId])[0][0]
        old_check = check_pass(old_pass,hashed_pass)
        if old_check :
            new_hashed = hash_pass(new_pass)
            return update_one_record("employees",{"password":new_hashed},"empId",self.empId)
        else:
            print("Old password did not match \n")
            return False

    def request_self_info_change(self,updated_info):
        # created_by integer NOT NULL, updated_info text NOT NULL, hr_assigned integer, approved_by_hr integer NOT NULL, remark text, created_at integer NOT NULL, update_commited integer NOT NULL
        all_hr = read_fields_from_record("employees","empId","user_type",["hr"])
        all_hr = [tuple_emp_id[0] for tuple_emp_id in all_hr ]
        # print(all_hr)
        request = {
            "created_by": self.empId,
            "updated_info": updated_info,
            "assigned_hr": random.choice(all_hr),
            "created_at": ceil(time.time()),
            "update_commited_at":0,
            "request_status":"hr_assigned",
            "remark":None,
        }
        created_request = write_to_table("requests",request)
        print("updated user will be ", created_request)
        return True

    @abstractmethod
    def info():
        pass



# name = "aryan"
# phone = "984783723"
# email = "aryan@gmail.com"
# address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}
# new_emp = employee(name,phone,email,address)
