from typing import is_typeddict
from .worker_ui import Worker_interface
from ..utils.general_utils import int_input, make_printable

from tabulate import tabulate


class Hr_interface(Worker_interface):
    def __init__(self, hr_employee):
        self.hr = hr_employee
        super().__init__(hr_employee)

    def show_menu(self):
        while True:
            op = int_input(f"""
            Welcome {self.hr.name} .....
                Press the number in front of the option to perform an action :-
                  1 : Open pending requests
                  2 : Show all closed requests 
                  3 : See my profile
                  4 : Search other employees
                  5 : See my team 
                  6 : Update password 
                  7 : Exit
                  """)
            if op == 1:
                self.open_pending_requests()
            elif op == 2:
                self.show_closed_requests()
            elif op == 3:
                self.see_my_profile()
            elif op == 4:
                self.search_other_employee()
            elif op == 5:
                self.see_own_team_ui(self.employee.empId)
            elif op == 6:
                self.update_password_ui()
            elif op == 7:
                exit()

    def open_pending_requests(self):
        requests = self.hr.get_pending_requests()
        if not requests:
            print("There are no pending requests")
        else:
            keys = [
                "request_id",
                "created_by",
                "assigned_hr",
                "remark",
                "update_committed_at",
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
                        "Remark",
                        "committed At",
                        "Created At",
                    ],
                )
            )

            pending_req_ids = [req[0] for req in printable_requests]
            while True:
                op = int_input(
                    "To approve a request press 1, to reject press 2, to see updated information press 3, to go back to previous menu hit 0 \n"
                )
                if op == 1:
                    self.update_req_ui("approve", pending_req_ids)
                elif op == 2:
                    self.update_req_ui("reject", pending_req_ids)
                elif op == 3:
                    req_id_for_details = int_input(
                        "Enter the request id you want to see the details of : "
                    )
                    print("yet to be implemented")
                elif op == 0:
                    self.show_menu()

    def update_req_ui(self, update_type, pending_req_ids):
        req_id = int_input(f"""To {update_type} a request please enter the request id and hit enter
            """)
        if req_id in pending_req_ids:
            remark = input("Please enter a remark for the request : ")
            self.hr.update_request_status(req_id, remark, update_type)
        else:
            print("Request not found please try again")

    def show_closed_requests(self):
        requests = self.hr.get_closed_requests()
        if not requests:
            print("There are no pending requests")
        else:
            keys = [
                "request_id",
                "created_by",
                "assigned_hr",
                "remark",
                "update_committed_at",
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
                        "Remark",
                        "committed At",
                        "Created At",
                    ],
                )
            )
