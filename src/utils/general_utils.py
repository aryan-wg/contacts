from .validations_utils import validate_pin_code, int_input

import bcrypt
import json


def get_address_input():
    address_dict = {}

    address_dict["street"] = input("Enter street : ")
    while True:
        address_dict["postal_code"] = int_input(
            "Enter postal code (must be a 6 digit integer) : "
        )

        if validate_pin_code(address_dict["postal_code"]):
            break
        else:
            print("Enter a valid pin code \n")

    address_dict["city"] = input("Enter city : ")
    address_dict["state"] = input("Enter state : ")
    address_dict["country"] = input("Enter country : ")
    address_str = json.dumps(address_dict)
    return address_str


def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

def check_pass(password, hashed_db):
    return bcrypt.checkpw(password.encode(), hashed_db)


def format_for_display(keys, original_data):
    printable_data = []
    for item in original_data:
        printable_item = []
        for key in keys:
            printable_item.append(item[key])
        printable_data.append(printable_item)

    return printable_data


def print_user_info_in_relation(relation, user_to_print):
    print(f"""
Name : {relation[user_to_print]["name"]}
Email : {relation[user_to_print]["email"]}
Phone : {relation[user_to_print]["phone"]}
Employee Id : {relation[user_to_print]["empId"]}
""")


def print_relation(relation):
    return True
    print(
        f'\n{relation["employee"]["name"]} with employee id {relation["employee"]["empId"]} reports to {relation["reports_to"]["name"]} with employee Id {relation["reports_to"]["empId"]}\n'
    )
