from abc import abstractmethod, ABC
import json
import time

from ...utils.general_utils import check_pass, hash_pass
from ...utils.async_pg_db_utils import (
    match_string_in_field,
    read_fields_from_record,
    update_one_record,
    write_to_table,
)
from math import ceil
import random


class Employee(ABC):
    # def __init__(self, employee_info):
    #     empId, name, phone, email, json_str_address, user_type = employee_info
    #     self.name = name
    #     self.phone = phone
    #     self.email = email
    #     self.empId = empId
    #     # this address will be a dict that has information
    #     # street,city,state,postal code, country
    #     parsed_address = json.loads(json_str_address)
    #     self.address = parsed_address
    #     self.user_type = user_type
    #     # print("new employee instantiated ", self.name)
    #     # print(self.name,self.phone,self.email,self.address)
    #

    def __init__(self):
        pass

    def get_profile_info(self):
        profile = {
            # "name": self.name,
            # "phone": self.phone,
            # "email": self.email,
            # "empId": self.empId,
            # "address": self.address,
        }
        return profile

    async def search_other_employee(self, name):
        data = await match_string_in_field(
            "employees", "empId, name, phone, email", "name", name
        )
        return data

    async def update_password(self, old_pass, new_pass, empId):
        hashed_pass = await read_fields_from_record(
            "employees", "password", "empId", [empId]
        )
        if hashed_pass:
            hashed_pass = hashed_pass[0][0]
        old_check = check_pass(old_pass, hashed_pass)
        if old_check:
            new_hashed = hash_pass(new_pass)
            return await update_one_record(
                "employees", {"password": new_hashed}, "empId", empId
            )
        else:
            print("Old password did not match \n")
            return False

    async def request_self_info_change(self, updated_info, empId):
        # created_by integer NOT NULL, updated_info text NOT NULL, hr_assigned integer, approved_by_hr integer NOT NULL, remark text, created_at integer NOT NULL, update_committed integer NOT NULL
        all_hr = await read_fields_from_record(
            "employees", "empId", "user_type", ["hr"]
        )
        try:
            all_hr = [tuple_emp_id[0] for tuple_emp_id in all_hr]
            if not all_hr:
                raise ValueError("No HR employee to assign request to.")
            else:
                assigned_hr = random.choice(all_hr)
                if len(all_hr) == 1:
                    if all_hr[0] == empId:
                        print(
                            "\nWarning - you are the only HR hence you will be approving your own request\n"
                        )
                        assigned_hr = empId
                else:
                    while assigned_hr == empId:
                        assigned_hr = random.choice(all_hr)
                request = {
                    "created_by": empId,
                    "updated_info": updated_info,
                    "assigned_hr": assigned_hr,
                    "created_at": ceil(time.time()),
                    "update_committed_at": 0,
                    "request_status": "hr_assigned",
                    "remark": None,
                }
                created_request = await write_to_table("requests", request)
                print("updated user will be ", created_request)
                return True

        except Exception as e:
            message = str(e)
            print(message)

    @abstractmethod
    def info():
        pass


# name = "aryan"
# phone = "984783723"
# email = "aryan@gmail.com"
# address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}
# new_emp = employee(name,phone,email,address)
