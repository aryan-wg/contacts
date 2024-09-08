from .worker_ui import WorkerUi
from ..utils.general_utils import int_input, format_for_display

from tabulate import tabulate

from ..constants import hr_requests_formatting_keys,hr_requests_tabulate_headers,request_info_formating_keys,request_info_tabulate_headers 
import json

from pprint import pprint

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
            match selection:
                case 1:
                    self.show_pending_requests()

                case 2:
                    self.show_closed_requests()

                case 3:
                    self.see_my_profile()

                case 4:
                    self.search_other_employee()

                case 5:
                    self.show_my_team(self.employee.empId)

                case 6:
                    self.update_password_ui()

                case 7:
                    exit()

    def show_pending_requests(self):
        requests = self.hr.get_pending_requests()
        if not requests:
            print("There are no pending requests.")
        else:
            formatted_requests = format_for_display(hr_requests_formatting_keys, requests)
            print(tabulate(formatted_requests, hr_requests_tabulate_headers))
            
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
                match selection:                
                    case 1:
                        self.change_req_status_input("approve", pending_req_ids)
                    case 2:
                        self.change_req_status_input("reject", pending_req_ids)
                    case 3:
                        req_details_id = int_input(
                            "\nEnter the request id you want to see the details of : "
                        )
                        self.show_request_details(req_details_id)
                    case 0:
                        return 

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
            printable_requests = format_for_display(hr_requests_formatting_keys, requests)
            print(tabulate(printable_requests, hr_requests_tabulate_headers))

    def show_request_details(self,reqId):
        requests = self.hr.get_pending_requests()
        for request in requests:
            if request["request_id"] == reqId:
                formatted_data = format_for_display(request_info_formating_keys, [json.loads(request["updated_info"])])
                address = json.loads(formatted_data[0][-1])
                str_address = ""
                for key, value in address.items():
                    str_address += f"{key} - {value} \n"

                formatted_data[0][-1] = str_address
                print("\n",
                    tabulate(
                        formatted_data,
                        request_info_tabulate_headers
                    )
                )


