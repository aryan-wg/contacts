from .worker_ui import Worker_interface
from ..utils.general_utils import make_printable

from tabulate import tabulate
class Hr_interface(Worker_interface):
    def __init__(self,hr_employee):
        self.hr = hr_employee
        super().__init__(hr_employee)

    def show_menue(self):
        while True:
            op = int(input(f"""
            Welcome {self.hr.name} .....
                Press the number in front of the option to perform an action :-
                  1 : Open pending requests
                  2 : Show all closed requests 
                  3 : See my profile
                  4 : Search other employees
                  5 : See my team 
                  6 : Exit
                  """)
            )
            if op == 1:
                self.open_pending_requests()
            elif op == 2:
                self.show_closed_reqests()
            elif op == 3:
                self.see_my_profile()
            elif op == 4:
                self.search_other_employee()
            elif op == 5:
                self.see_own_team()
                self.show_menue()
            elif op == 6:
                exit()
    def open_pending_requests(self):
        requests = self.hr.pending_req
        if not requests:
            print("There are no pending requests")
        else :
            keys = ["request_id","created_by","assigned_hr","remark","update_commited_at","created_at",]
            printable_requests = make_printable(keys,requests)
            print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Remark","Commited At","Created At"]))

            pending_req_ids = [ req[0] for req in printable_requests ]
            while True:
                op = int(input("To approve a request press 1, to reject press 2 to go back to previous menue hit 0 \n"))
                if op == 1: 
                    self.update_req_ui("approve",pending_req_ids)
                elif op == 2:
                    self.update_req_ui("reject",pending_req_ids)
                elif op == 0:
                    self.show_menue()

    def update_req_ui(self,type,pending_req_ids):
        req_id = int(input((f"""To {type} a request please enter the request id and hit enter
        """)))
        if req_id in pending_req_ids:
            remark = input("Please enter a remak for the request : ")
            self.hr.update_request_status(req_id,remark,type)
        else :
            print("Request not found please try again")

    def show_closed_reqests(self):
        requests = self.hr.closed_req
        if not requests:
            print("There are no pending requests")
        else:
            keys = ["request_id","created_by","assigned_hr","remark","update_commited_at","created_at",]
            printable_requests = make_printable(keys,requests)
            print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Remark","Commited At","Created At"]))
