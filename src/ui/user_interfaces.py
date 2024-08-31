from pprint import pprint
from ..utils.general_utils import make_printable,take_address_input
from ..auth import Auth
from tabulate import tabulate

class Admin_interface:
    def __init__(self, admin):
        self.admin = admin

    def show_menue(self):
        while True:
            op = int(input(f"""
            Welcome {self.admin.name} .....
                Press the number in front of the option to perform an action :-
                  1 : Open pending requests
                  2 : Create a new worker
                  3 : Create a new HR employee
                  4 : Show all commited requests
                  5 : Exit
                  """)
            )
            if op == 1:
                self.open_pending_requests()
            elif op == 2:
                self.create_worker_form()
            elif op == 3:
                self.create_hr_employee()
            elif op == 4:
                self.show_all_commited()
            elif op == 5:
                exit()
    
    def show_all_commited(self):
        requests = self.admin.closed_req
        keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
        printable_requests = make_printable(keys,requests)
        print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))

    def open_pending_requests(self):
        requests = self.admin.pending_req
        if not requests:
            print("There are no pending requests")
        else :
            keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
            printable_requests = make_printable(keys,requests)
            print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))
            
            pending_req_ids = [ req[0] for req in printable_requests ]
            while True:
                req_id = int(input(("""To commit a request please enter the request id or and hit enter
                *If you want to got to preivious menue press 0 
                """)))
                if req_id in pending_req_ids:
                    self.admin.commit_request(req_id)
                elif req_id == 0:
                    # can also change this to go to prev menue in future
                    self.show_menue()
                else :
                    print("Request not found please try again")

    def create_worker_form(self):
        print("-----------------Creatting a new worker-----------------")
        worker_dict = {}
        worker_dict["name"] = input("Enter worker name : ")
        worker_dict["phone"] = int(input("Enter worker's phone number : "))
        worker_dict["email"]  = input("Enter worker's email address : ")
        worker_dict["address"]= take_address_input()
        worker_dict["password"] = input("Enter worker's initial password : ")
        
        self.admin.create_new_worker(worker_dict)
        return True 
        
    def create_hr_employee(self):
        pass

class Worker_interface:
    def __init__(self):
        pass

    def show_menue(self):
        print("""this is the menue of worker""")


class Hr_interface:
    def __init__(self):
        pass

    def show_menue(self):
        print("""this is the menue of hr""")


class Auth_interface:
    def __init__(self):
        print("this is the auth interface")

    def get_credentials(self):
        empId = int(input("""Please enter your employee id : """))
        password = input("""Please enter your password: """)
        return (empId, password)

    def login(self):
        user_obj = None
        print("hello")
        while not user_obj :
            empId, password = self.get_credentials()
            auth_obj = Auth(empId,password)
            user_obj = auth_obj.login()
        print(user_obj)
        return user_obj 

# printable_requests = []
# for request in requests:
#     printable_req = []
#     for key in keys:
#         printable_req.append(request[key]) 
#     printable_requests.append(printable_req)
#     
