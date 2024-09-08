from ..ui.employee_ui import EmployeeUi
from ..utils.validations_utils import (
    int_input,
)
from ..utils.input_utils import phone_input,email_input,password_input

from ..utils.general_utils import (
    format_for_display,
    get_address_input
    )
from ..constants import admin_requests_tabulate_headers,admin_requests_formatting_kyes

from tabulate import tabulate

import json


class AdminUi(EmployeeUi):
    def __init__(self, admin):
        super().__init__(admin)
        self.admin = admin

    def show_menu(self):
        while True:
            selected = int_input(
f"""
----------------------------------------------------------------------------------------------
Welcome {self.employee.name} .....
    Press the number in front of option to perform an action :-
      1 : Open pending requests
      2 : Create a new employee 
      3 : Show all committed requests
      4 : Search for employees 
      5 : Show my profile
      6 : Update password
      7 : Exit  
----------------------------------------------------------------------------------------------
"""             )
            match selected:
                case 1:
                    self.open_pending_requests()
                case 2:
                    self.create_employee_form()
                case 3:
                    self.show_all_committed()
                case 4:
                    self.search_other_employee()
                case 5:
                    self.see_my_profile()
                case 6:
                    self.update_password_ui()
                case 7:
                    exit()

    def show_all_committed(self):
        requests = self.admin.get_closed_req()
        if requests:
            printable_requests = format_for_display(admin_requests_formatting_kyes, requests)
            print(
                tabulate(
                    printable_requests,
                    admin_requests_tabulate_headers 
                )
            )
        else:
            print("\nNo request committed yet\n")

    def open_pending_requests(self):
        requests = self.admin.get_pending_req()
        if not requests:
            print("\nThere are no pending requests\n")
        else:
            formatted_requests = format_for_display(admin_requests_formatting_kyes, requests)
            print(
                tabulate(
                    formatted_requests,
                    admin_requests_tabulate_headers 
                )
            )

            pending_req_ids = [req[0] for req in formatted_requests]
            req_id = int_input("""\nTo commit a request please enter the request id and hit enter
            *If you want to got to previous menu press 0
            """)
            if req_id in pending_req_ids:
                self.admin.commit_request(req_id)
            elif req_id == 0:
                return 
            else:
                print("\nRequest not found please try again\n")

    def create_employee_form(self):
        print("--------------------------------Creating a new employee--------------------------------")
        worker_dict = {}

        worker_dict = self.__user_type_input(worker_dict)
        worker_dict["name"] = input(f"Enter {worker_dict["user_type"]}'s name : ")
        worker_dict = phone_input(worker_dict)
        worker_dict = email_input(worker_dict)
        worker_dict["address"] = json.dumps(get_address_input())
        worker_dict = password_input(worker_dict)

        created_worker = self.admin.create_new_employee(worker_dict)

        new_emp_id = created_worker[0]
        new_emp_name = created_worker[-1]

        created_relation = None
        while not created_relation:
            print(
                f"New {new_emp_name} employee created with employee id {new_emp_id} (please take note of employee id as it is required for login)\n"
            )
            reports_to = int_input(
                f"Enter the employee id of the person who {worker_dict["name"]} reports to : "
            )
            created_relation = self.admin.create_new_relation(new_emp_id, reports_to)
            if not created_relation:
                print("\nReporting to user does not exsist try again.\n")
                continue
            else :
                print(
                    f"Employee with id {created_relation[1]} is now reporting to {created_relation[0]}"
                )

    def __user_type_input(self,worker_dict):
        user_type_input = int_input(
"""
1 : Make a HR type user
2 : Make a Worker type user

"""
        )
        while True:
            if user_type_input == 1:
                worker_dict["user_type"] = "hr"
                return worker_dict
            elif user_type_input == 2:
                worker_dict["user_type"] = "worker"
                return worker_dict
            else:
                print("Enter a valid input ")

