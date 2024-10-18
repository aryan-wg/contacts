from abc import abstractmethod, ABC
import json
import time

from ...types.general_types import LOG_LEVEL_ENUM
from ...utils.parsing_populating_utils import parse_requests, populate_requests

from ...utils.general_utils import check_pass, hash_pass
from ...utils.async_pg_db_utils import (
    check_if_exists_in_db,
    match_string_in_field,
    read_by_multiple_att_and_keys,
    read_fields_from_record,
    update_one_record,
    write_to_table,
)
from math import ceil
import random


class Employee:
    # def __init__(self, employee_info):
    #     self.emp_id, name, phone, email, json_str_address, user_type = employee_info
    #     self.name = name
    #     self.phone = phone
    #     self.email = email
    #     self.self.emp_id = empId
    #     # this address will be a dict that has information
    #     # street,city,state,postal code, country
    #     parsed_address = json.loads(json_str_address)
    #     self.address = parsed_address
    #     self.user_type = user_type
    #     # print("new employee instantiated ", self.name)
    #     # print(self.name,self.phone,self.email,self.address)
    #

    def __init__(self, emp_id,logger):
        self.emp_id = emp_id
        self.logger = logger

    async def get_profile_info(self):
        data = await read_fields_from_record(
            "employees", "name,phone,email,address", "empId", [self.emp_id]
        )
        if len(data) == 1:
            data = data[0]
            profile = {
                "name": data[0],
                "phone": data[1],
                "email": data[2],
                "address": json.loads(data[3]),
                "emp_id": self.emp_id,
            }
            self.logger.log("get_profile_info",LOG_LEVEL_ENUM.INFO)
            return profile
        else:
            self.logger.log("get_profile_info User does not exist")
            raise ValueError("User does not exist")

    async def search_other_employee(self, name):
        employees = await match_string_in_field(
            "employees", "empid, name, phone, email", "name", name
        )
        self.logger.log("Search other employee",LOG_LEVEL_ENUM.INFO)
        return employees

    async def update_password(self,emp_id, old_pass, new_pass):
        if await check_if_exists_in_db("employees","empId",emp_id):
            hashed_pass = await read_fields_from_record(
                "employees", "password", "empId", [emp_id]
            )
            if hashed_pass:
                hashed_pass = hashed_pass[0][0]
            old_check = check_pass(old_pass, hashed_pass)
            if old_check:
                new_hashed = hash_pass(new_pass)
                self.logger.log("Updated password",LOG_LEVEL_ENUM.INFO)
                return await update_one_record(
                    "employees", {"password": new_hashed}, "empId",emp_id
                )
            else:
                self.logger.log("update_password Old passwords did not match",LOG_LEVEL_ENUM.ERROR)
                raise ValueError("Unauthorized user")
        else:
            self.logger.log("update_password Employee not found",LOG_LEVEL_ENUM.ERROR)
            raise ValueError("Unauthorized user")

    async def request_self_info_change(self, updated_info):
        is_request_in_progress = await read_by_multiple_att_and_keys(
            "requests",
            "created_by",
            ["created_by", "request_status"],
            [self.emp_id, ["approved_by_hr", "hr_assigned"]],
        )
        if not len(is_request_in_progress) == 0:
            self.logger("One request already under process",LOG_LEVEL_ENUM.ERROR)
            raise ValueError("One request already under process")
        else:
            all_hr = await read_fields_from_record(
                "employees", "empId", "user_type", ["hr"]
            )
            all_hr = [tuple_emp_id[0] for tuple_emp_id in all_hr]
            if not all_hr:
                self.logger("No HR in to assign request to", LOG_LEVEL_ENUM.ERROR)
                raise ValueError("No HR employee to assign request to.")
            else:
                assigned_hr = random.choice(all_hr)
                if len(all_hr) == 1:
                    if all_hr[0] == self.emp_id:
                        # print(
                        #     "\nWarning - you are the only HR hence you will be approving your own request\n"
                        # )
                        assigned_hr = self.emp_id
                else:
                    while assigned_hr == self.emp_id:
                        assigned_hr = random.choice(all_hr)
                request = {
                    "created_by": self.emp_id,
                    "updated_info": json.dumps(updated_info),
                    "assigned_hr": assigned_hr,
                    "created_at": ceil(time.time()),
                    "update_committed_at": 0,
                    "request_status": "hr_assigned",
                    "remark": None,
                }
                created_request = await write_to_table("requests", request)
                self.logger.log("New request created",LOG_LEVEL_ENUM.INFO)
                return created_request[0]

    async def get_my_requests(self, current_status_list):
        requests = await read_by_multiple_att_and_keys(
            "requests",
            "*",
            ["created_by", "request_status"],
            [self.emp_id, current_status_list],
        )
        requests = parse_requests(requests)
        requests = await populate_requests(requests)
        self.logger.log(f"Get my requests {current_status_list}",LOG_LEVEL_ENUM.INFO)
        return requests

    @abstractmethod
    def info():
        pass


# name = "aryan"
# phone = "984783723"
# email = "aryan@gmail.com"
# address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}
# new_emp = employee(name,phone,email,address)
