from .worker_ui import WorkerUi
from ..utils.general_utils import int_input, format_for_display

from tabulate import tabulate

from ..constants import requests_formatting_keys_hr, tabulate_requests_headers_hr


class HrUi(WorkerUi):
    def __init__(self, hr_employee):
        self.hr = hr_employee
        super().__init__(hr_employee)

    def show_menu(self):
        while True:
            selection = int_input(
f"""
-----------------------------------------------------------------------------------------------
Welcome {self.hr.name} .....

1 : Open pending requests
2 : Show all closed requests 
3 : See my profile
4 : Search other employees
5 : See my team 
6 : Update password 
7 : Exit
-----------------------------------------------------------------------------------------------
                """)
            if selection == 1:
                self.show_pending_requests()

            elif selection == 2:
                self.show_closed_requests()

            elif selection == 3:
                self.see_my_profile()

            elif selection == 4:
                self.search_other_employee()

            elif selection == 5:
                self.see_own_team_ui(self.employee.empId)

            elif selection == 6:
                self.update_password_ui()

            elif selection == 7:
                exit()

    def show_pending_requests(self):
        requests = self.hr.get_pending_requests()
        if not requests:
            print("There are no pending requests.")
        else:
            formatted_requests = format_for_display(requests_formatting_keys_hr, requests)
            print(tabulate(formatted_requests, tabulate_requests_headers_hr))
            
            pending_req_ids = [req[0] for req in formatted_requests]
            while True:
                selection = int_input(
"""
-----------------------------------------------------------------------------------------------
1 : Approve a request
2 : Reject a request
3 : See request information
0 : Previous menu 
-----------------------------------------------------------------------------------------------
"""
                )
                if selection == 1:
                    self.change_req_status_input("approve", pending_req_ids)
                elif selection == 2:
                    self.change_req_status_input("reject", pending_req_ids)
                elif selection == 3:
                    req_id_for_details = int_input(
                        "Enter the request id you want to see the details of : "
                    )
                    print("yet to be implemented")
                elif selection == 0:
                    self.show_menu()

    def change_req_status_input(self, update_type, pending_req_ids):
        req_id = int_input(f"To {update_type} a request please enter the request id and hit enter : ")
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
            printable_requests = format_for_display(requests_formatting_keys_hr, requests)
            print(tabulate(printable_requests, tabulate_requests_headers_hr))
