from tabulate import tabulate
from ..utils.validations_utils import (
    validate_email,
    validate_phone,
    int_input,
    validate_password,
)
from ..utils.general_utils import (
    format_for_display,
    get_address_input,
)
import json
import maskpass


class EmployeeUi:
    def __init__(self, employee):
        self.employee = employee

    def see_my_profile(self):
        profile_info = self.employee.get_profile_info()
        my_profile_formating_keys = ["name", "phone", "email", "empId", "address"]

        formatted_data = format_for_display(keys, [profile_info])
        address = json.loads(formatted_data[0][-1])
        str_address = ""
        for key, value in address.items():
            str_address += f"{key} - {value} \n"

        formatted_data[0][-1] = str_address
        print(
            tabulate(
                formatted_data,
                headers=["Name", "Phone Number", "Email", "Employee ID", "Address"],
            )
        )

        op = int_input(
            "\nTo request for a change in information press 1, to go back press 0 : "
        )
        if op == 0:
            return 
        elif op == 1:
            self.update_profile_input()

    def update_password_input(self):
        old_pass = maskpass.askpass("Enter your current password : ")
        new_pass = maskpass.askpass(
""" 
Password must have - 8 Characters, 1 Uppercase letter, 1 Lowercase letter, 1 Number, 1 Special character
Enter new password -
""")
        if validate_password(new_pass):
            if self.employee.update_password(old_pass, new_pass):
                if True:
                    print("Password updated successfully \n")
            else:
                print("Password could not be updated \n")
        else:
            print("Invalid new password")
        self.show_menu()

    def update_profile_input(self):
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

        worker_dict["address"] = get_address_input()

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
            self.show_menu()
        else:
            headers = ["Emp Id", "Name", "Phone No", "Email"]
            print(tabulate(search_result, headers))
            self.show_menu()
