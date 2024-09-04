from .db_utils import read_fields_from_record
from datetime import datetime, time

import bcrypt
import json
import re


def int_input(message):
    while True:
        input_num = input(message)
        # print(input_num.isdigit())
        if input_num.isdigit():
            return int(input_num)
        else:
            print("Invalid input try again")


def take_address_input():
    address_dict = {}

    address_dict["street"] = input("Enter street : ")

    # address_dict["postal_code"] = int_input(
    #     "Enter postal code (must be a 6 digit integer) : "
    # )
    while True:
        address_dict["postal_code"] = int_input("Enter postal code (must be a 6 digit integer) : ")

        if validate_pin_code(address_dict["postal_code"]):
            break
        else:
            print("Enter a valid pin code \n")

    address_dict["city"] = input("Enter city : ")
    address_dict["state"] = input("Enter state : ")
    address_dict["country"] = input("Enter country : ")
    address_str = json.dumps(address_dict)
    return address_str

def validate_email(email):
    return re.fullmatch(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email)


def validate_phone(phone):
    phone_str = str(phone)
    return re.fullmatch(r"^\d{10}$", phone_str)


def validate_pin_code(pin):
    pin_str = str(pin)
    return re.fullmatch(r"^d{6}$", pin_str)


def validate_password(password):
    return re.search(r"^(?=.*[A-Z](?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8}$", password)


def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode("utf-8")


def check_pass(password, hashed_db):
    return bcrypt.checkpw(password.encode(), hashed_db.encode())


def make_printable(keys, original_data):
    printable_data = []
    for item in original_data:
        printable_item = []
        for key in keys:
            printable_item.append(item[key])
        printable_data.append(printable_item)

    return printable_data


def parse_requests(requests):
    print(requests)
    requests_parsed = []
    for request in requests:
        temp = {
            "request_id": request[0],
            "created_by": request[1],
            "updated_info": request[2],
            "assigned_hr": request[3],
            "remark": request[4],
            "created_at": request[5],
            "update_commited_at": request[6],
            "request_status": request[7],
        }
        requests_parsed.append(temp)

    return requests_parsed


def populate_requests(requests):
    populated = []
    for request in requests:
        time_stamp = datetime.fromtimestamp(request["created_at"])
        request["created_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        if not request["update_commited_at"] == 0:
            time_stamp = datetime.fromtimestamp(request["update_commited_at"])
            request["update_commited_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        record = read_fields_from_record(
            "employees",
            "name",
            "empId",
            [request["created_by"], request["assigned_hr"]],
        )
        request["created_by"] = record[0][0]
        request["assigned_hr"] = record[1][0]
        # print(request)
        populated.append(request)
    return populated


def parse_relations(relations):
    relations_parsed = []
    for relation in relations:
        temp = {
            "reports_to": relation[0],
            "empId": relation[1],
            "team": relation[2],
        }
        relations_parsed.append(temp)

    return relations_parsed


def populate_relations(relations):
    populated = []
    for relation in relations:
        if relation["reports_to"] == 0:
            reports_to = {
                "name": None,
                "empId": None,
                "email": None,
                "phone": None,
            }
            relation["reports_to"] = reports_to

        else:
            reports_to_info = read_fields_from_record(
                "employees", "name, email, phone", "empId", [relation["reports_to"]]
            )
            if reports_to_info:
                reports_to = {
                    "name": reports_to_info[0][0],
                    "empId": relation["reports_to"],
                    "email": reports_to_info[0][1],
                    "phone": reports_to_info[0][2],
                }
                relation["reports_to"] = reports_to

        emp_info = read_fields_from_record(
            "employees", "name, email, phone", "empId", [relation["empId"]]
        )
        employee = {
            "name": emp_info[0][0],
            "empId": relation["empId"],
            "email": emp_info[0][1],
            "phone": emp_info[0][2],
        }
        relation["employee"] = employee
        populated.append(relation)
    return populated
