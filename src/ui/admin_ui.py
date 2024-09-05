from ..ui.employee_interface import EmployeeInterface
from ..utils.general_utils import (
    validate_email,
    validate_phone,
    make_printable,
    take_address_input,
    int_input,
)
from tabulate import tabulate
import json


class Admin_interface(EmployeeInterface):
    def __init__(self, admin):
        super().__init__(admin)
        self.admin = admin

    def show_menue(self):
        while True:
            op = int_input(f"""
            Welcome {self.employee.name} .....
                Press the number in front of the option to perform an action :-
                  1 : Open pending requests
                  2 : Create a new employee 
                  3 : Show all commited requests
                  4 : Search for empoloyees 
                  5 : Show my profile
                  6 : Update password
                  7 : Exit  
                  """)
            if op == 1:
                self.open_pending_requests()
            elif op == 2:
                self.create_employee_form()
            elif op == 3:
                self.show_all_commited()
            elif op == 4:
                self.search_other_employee()
                self.show_menue()
            elif op == 5:
                self.see_my_profile()
            elif op == 6:
                self.update_password_ui()
            elif op == 7:
                exit()

    def show_all_commited(self):
        requests = self.admin.get_closed_req()
        keys = [
            "request_id",
            "created_by",
            "assigned_hr",
            "update_commited_at",
            "created_at",
        ]
        if requests:
            printable_requests = make_printable(keys, requests)
            print(
                tabulate(
                    printable_requests,
                    headers=[
                        "Request Id",
                        "Created By",
                        "Assigned HR",
                        "Commited At",
                        "Created At",
                    ],
                )
            )
        else:
            print("No reques commited yet")

    def open_pending_requests(self):
        requests = self.admin.get_pending_req()
        if not requests:
            print("There are no pending requests")
        else:
            keys = [
                "request_id",
                "created_by",
                "assigned_hr",
                "update_commited_at",
                "created_at",
            ]
            printable_requests = make_printable(keys, requests)
            print(
                tabulate(
                    printable_requests,
                    headers=[
                        "Request Id",
                        "Created By",
                        "Assigned HR",
                        "Commited At",
                        "Created At",
                    ],
                )
            )

            pending_req_ids = [req[0] for req in printable_requests]
            req_id = int_input("""To commit a request please enter the request id and hit enter
            *If you want to got to preivious menue press 0 
            """)
            if req_id in pending_req_ids:
                self.admin.commit_request(req_id)
            elif req_id == 0:
                # can also change this to go to prev menue in future
                self.show_menue()
            else:
                print("Request not found please try again")

    def create_employee_form(self):
        print("-----------------Creatting a new employee-----------------")
        user_type_input = int_input(
            "Enter press 1 to create worker and 0 to create HR employee : "
        )
        worker_dict = {}
        while True:
            if user_type_input == 0:
                worker_dict["user_type"] = "hr"
                break
            elif user_type_input == 1:
                worker_dict["user_type"] = "worker"
                break
            else:
                print("Enter a valid input ")

        worker_dict["name"] = input(f"Enter {worker_dict["user_type"]}'s name : ")

        # worker_dict["phone"] = int_input(f"Enter {worker_dict["user_type"]}'s phone number : ")
        while True:
            worker_dict["phone"] = input(
                f"Enter {worker_dict["user_type"]}'s phone number : "
            )
            if worker_dict["phone"].isdigit():
                if validate_phone(worker_dict["phone"]):
                    break
                else:
                    print("Enter a valid phone number")
            else:
                print("Enter a valid phone number")

        # worker_dict["email"]  = input(f"Enter {worker_dict["user_type"]}'s email address : ")
        while True:
            worker_dict["email"] = input(
                f"Enter {worker_dict["user_type"]}'s email address : "
            )

            if validate_email(worker_dict["email"]):
                break
            else:
                print("Enter a valid email")

        worker_dict["address"] = json.dumps(take_address_input())

        worker_dict["password"] = input(
            f"Enter {worker_dict["user_type"]}'s initial password \n(must be 8 char long and contain 1 digit, 1 lowercase, 1 uppercase, 1 special character) : "
        )
        # while True:
        #     worker_dict["password"] = input(f"Enter {worker_dict["user_type"]}'s initial password \n(must be 8 char long and contain 1 digit, 1 lowercase, 1 uppercase, 1 special character) : ")
        #
        #     if validate_password(worker_dict["password"]):
        #         break
        #     else:
        #         print("Enter a valid email")

        created_worker = self.admin.create_new_employee(worker_dict)

        new_emp_id = created_worker[0]
        new_emp_name = created_worker[-1]

        print(
            f"New {new_emp_name} employee created with employee id {new_emp_id} (please take note of employee id as it is requeired for login)\n"
        )
        reports_to = int_input(
            f"Enter the employee id of the person who {worker_dict["name"]} reports to : "
        )

        created_relation = self.admin.create_new_relation(new_emp_id, reports_to)
        print(
            f"Employee with id {created_relation[1]} is now reporting to {created_relation[0]}"
        )
        return True
