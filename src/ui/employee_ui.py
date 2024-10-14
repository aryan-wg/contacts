from tabulate import tabulate

from ..utils.input_utils import email_input, password_input, phone_input
from ..utils.validations_utils import int_input

from ..utils.general_utils import (
    format_for_display,
    get_address_input,
)

from ..constants import my_profile_formating_keys,my_profile_tabulate_headers,search_employee_tabulate_headers

import json
import maskpass


class EmployeeUi:
    def __init__(self, employee):
        self.employee = employee

    def see_my_profile(self):
        profile_info = self.employee.get_profile_info()

        formatted_data = format_for_display(my_profile_formating_keys, [profile_info])
        address = json.loads(formatted_data[0][-1])
        str_address = ""
        for key, value in address.items():
            str_address += f"{key} - {value} \n"

        formatted_data[0][-1] = str_address
        print("\n",
            tabulate(
                formatted_data,
                my_profile_tabulate_headers
            )
        )

        selected = int_input(
                "\n1 : Request change in information \n0 : go back press \n"
        )
        if selected == 0:
            return  
        elif selected == 1:
            self.update_profile_input()

    def update_password_input(self):
        passwords = {"user_type":self.employee.user_type}
        passwords["old_pass"] = maskpass.askpass("Enter your current password : ")
        passwords = password_input(passwords)
        if self.employee.update_password(passwords["old_pass"], passwords["password"]):
            if True:
                print("Password updated successfully \n")
        else:
            print("Password could not be updated \n")

    def update_profile_input(self):
        worker_dict = {}
        worker_dict["user_type"] = self.employee.user_type
        worker_dict["name"] = input("Enter your name : ")
        worker_dict = phone_input(worker_dict)
        worker_dict  = email_input(worker_dict)
        worker_dict["address"] = get_address_input()

        success = self.employee.request_self_info_change(worker_dict)
        if success:
            print("Request created ")
            self.see_my_profile()
        else:
            print("There has been some error in creating a request")
            self.see_my_profile()

    def search_other_employee(self):
        name = input("\nEnter the name of user you want to search for : ")
        search_result = self.employee.search_other_employee(name)
        if not len(search_result):
            print("\nNo such users found\n")
            return 
        else:
            print("\n",tabulate(search_result, search_employee_tabulate_headers))
            return 
