from tabulate import tabulate
from ..utils.general_utils import (
    validate_email,
    validate_phone,
    int_input,
    make_printable,
    take_address_input,
    validate_password,
)
import json
import maskpass


class EmployeeInterface:
    def __init__(self, employee):
        self.employee = employee

    def see_my_profile(self):
        profile_info = self.employee.get_profile_info()
        keys = ["name", "phone", "email", "empId", "address"]
        printable_data_list = make_printable(keys, [profile_info])
        # address_keys = ["city","street","state","postal_code","country"]
        address = json.loads(printable_data_list[0][-1])
        # print(type(address))
        str_address = ""
        for key, value in address.items():
            str_address += f"{key} - {value} \n"

        printable_data_list[0][-1] = str_address
        print(
            tabulate(
                printable_data_list,
                headers=["Name", "Phone Number", "Email", "Employee ID", "Address"],
            )
        )

        op = int_input(
            "\nTo request for a change in information press 1, to go back press 0 : "
        )
        if op == 0:
            self.show_menue()
        elif op == 1:
            self.update_info_ui()
            # keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]

    def update_password_ui(self):
        old_pass = maskpass.askpass("Enter your current password : ")
        new_pass = maskpass.askpass(""" Enter new password -
                                **password must have -
            8 Characters, 1 Upparcase character, 1 Lowercase character, 1 Number, 1 Special character
                                """)
        if validate_password(new_pass):
            if self.employee.update_password(old_pass, new_pass):
                if True:
                    print("Password updated succesfully \n")
            else:
                print("Password could not be updated \n")
        else:
            print("Invalid new password")
        self.show_menue()

    def update_info_ui(self):
        worker_dict = {}
        worker_dict["name"] = input("Enter worker name : ")
        # worker_dict["phone"] = int_input(f"Enter {self.employee.user_type}'s phone number : ")
        while True:
            worker_dict["phone"] = int_input(
                f"Enter {self.employee.user_type}'s phone number : "
            )
            if validate_phone(worker_dict["phone"]):
                break
            else:
                print("Enter a valid phone number")

        # worker_dict["email"]  = input(f"Enter {self.employee.user_type}'s email address : ")
        while True:
            worker_dict["email"] = input(
                f"Enter {self.employee.user_type}'s email address : "
            )

            if validate_email(worker_dict["email"]):
                break
            else:
                print("Enter a valid email")

        worker_dict["address"] = take_address_input()

        success = self.employee.request_self_info_change(json.dumps(worker_dict))
        if success:
            print("Request created ")
            self.see_my_profile()
        else:
            print("There has been some error in creating a request")
            self.see_my_profile()

    def search_other_employee(self):
        name = input("Enter the name of user you want to search for : ")
        search_result = self.employee.search_other_employee(name)
        if not len(search_result):
            print("No such users found ")
            self.show_menue()
        else:
            headers = ["Emp Id", "Name", "Phone No", "Email"]
            print(tabulate(search_result, headers))
            self.show_menue()
