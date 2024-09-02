from pprint import pprint
from ..utils.general_utils import make_printable,take_address_input, validate_email, validate_phone ,validate_password
from ..auth import Auth
from tabulate import tabulate
import json
# class Admin_interface:
#     def __init__(self, admin):
#         self.admin = admin
#
#     def show_menue(self):
#         while True:
#             op = int(input(f"""
#             Welcome {self.admin.name} .....
#                 Press the number in front of the option to perform an action :-
#                   1 : Open pending requests
#                   2 : Create a new employee 
#                   3 : Show all commited requests
#                   4 : Exit
#                   5 : Testing fn
#                   """)
#             )
#             if op == 1:
#                 self.open_pending_requests()
#             elif op == 2:
#                 self.create_employee_form()
#             elif op == 3:
#                 self.show_all_commited()
#             elif op == 4:
#                 exit()
#             elif op == 5:
#                 self.testing_fn()
#             # elif op == 6:
#                  
#     def show_all_commited(self):
#         requests = self.admin.closed_req
#         keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
#         printable_requests = make_printable(keys,requests)
#         print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))
#
#     def open_pending_requests(self):
#         requests = self.admin.pending_req
#         if not requests:
#             print("There are no pending requests")
#         else :
#             keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
#             printable_requests = make_printable(keys,requests)
#             print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))
#             
#             pending_req_ids = [ req[0] for req in printable_requests ]
#             while True:
#                 req_id = int(input(("""To commit a request please enter the request id and hit enter
#                 *If you want to got to preivious menue press 0 
#                 """)))
#                 if req_id in pending_req_ids:
#                     self.admin.commit_request(req_id)
#                 elif req_id == 0:
#                     # can also change this to go to prev menue in future
#                     self.show_menue()
#                 else :
#                     print("Request not found please try again")
#
#     def testing_fn(self):
#         print("tesint fn is empty")
#
#     def create_employee_form(self):
#         print("-----------------Creatting a new employee-----------------")
#         user_type_input = int(input("Enter press 1 to create worker and 0 to create HR employee"))
#         worker_dict ={}
#         worker_dict["user_type"] = "hr" if user_type_input == 0 else "worker"
#         worker_dict["name"] = input(f"Enter {worker_dict["user_type"]}'s name : ")
#
#         worker_dict["phone"] = int(input(f"Enter {worker_dict["user_type"]}'s phone number : "))
#         # while True:
#         #     worker_dict["phone"] = int(input(f"Enter {worker_dict["user_type"]}'s phone number : "))
#         #
#         #     if validate_phone(worker_dict["phone"]):
#         #        break 
#         #     else :
#         #         print("Enter a valid phone number")
#         #     worker_dict["email"]  = input(f"Enter {worker_dict["user_type"]}'s email address : ")
#
#         worker_dict["email"]  = input(f"Enter {worker_dict["user_type"]}'s email address : ")
#         # while True:
#         #     worker_dict["email"]  = input(f"Enter {worker_dict["user_type"]}'s email address : ")
#         #
#         #     if validate_email(worker_dict["email"]):
#         #         break
#         #     else:
#         #         print("Enter a valid email")
#
#         worker_dict["address"] = json.dumps(take_address_input())
#
#         worker_dict["password"] = input(f"Enter {worker_dict["user_type"]}'s initial password \n(must be 8 char long and contain 1 digit, 1 lowercase, 1 uppercase, 1 special character) : ")
#         # while True:
#         #     worker_dict["password"] = input(f"Enter {worker_dict["user_type"]}'s initial password \n(must be 8 char long and contain 1 digit, 1 lowercase, 1 uppercase, 1 special character) : ")
#         #
#         #     if validate_password(worker_dict["password"]):
#         #         break
#         #     else:
#         #         print("Enter a valid email")
#
#         created_worker = self.admin.create_new_employee(worker_dict)
#
#         new_emp_id = created_worker[0]
#         new_emp_name = created_worker[-1]
#
#         print(f"New {new_emp_name} employee created with employee id {new_emp_id} (please take note of employee id as it is requeired for login)\n")
#         reports_to = int(input(f"Enter the employee id of the person who {worker_dict["name"]} reports to : "))
#         created_relation = self.admin.create_new_relation(new_emp_id,reports_to) 
#         print(f"Employee with id {created_relation[1]} is now reporting to {created_relation[0]}")
#         return True 
        
# class Worker_interface:
#     def __init__(self,worker):
#         self.worker = worker
#
#     def show_menue(self):
#         op = int(input(f"""
#         Welcome {self.worker.name} .....
#             Press the number in front of the option to perform an action :-
#               1 : See my profile 
#               2 : Search an employee
#               3 : See own team
#               4 : Exit
#               5 : 
#               """)
#         )
#         if op == 1:
#             self.see_my_profile()
#         elif op == 2:
#             self.search_other_employee()
#         elif op == 3:
#             self.see_own_team()
#         elif op == 4:
#             exit()
#
#     def see_my_profile(self):
#         profile_info = self.worker.get_profile_info()
#         keys = ["name","phone","email","empId","address"]
#         printable_data_list = make_printable(keys,[profile_info])
#         # address_keys = ["city","street","state","postal_code","country"]
#         address = json.loads(printable_data_list[0][-1])
#         # print(type(address))
#         str_address = ""
#         for key,value in address.items():
#             str_address+=f"{key} - {value} \n"
#
#         printable_data_list[0][-1] = str_address
#         print(tabulate(printable_data_list,headers=["Name","Phone Number","Email","Employee ID","Address"]))
#
#         op = int(input("\nTo request for a change in information press 1, to go back press 0 : "))
#         if op == 0:
#             self.show_menue()
#         elif op == 1:
#             self.update_info_ui()
#         #keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
#         # printable_requests = make_printable(keys,requests)
#         # print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))
#
#         pass
#
#     def search_other_employee(self):
#         pass
#     
#     def update_info_ui(self):
#         worker_dict ={}
#         worker_dict["name"] = input("Enter worker name : ")
#         worker_dict["phone"] = int(input("Enter worker's phone number : "))
#         worker_dict["email"]  = input("Enter worker's email address : ")
#         worker_dict["address"]= take_address_input()
#
#         success = self.worker.request_self_info_change(json.dumps(worker_dict))
#         if success:
#             self.see_my_profile()
#         else :
#             print("There has been some error in creating a request")
#             self.see_my_profile()
#
#     def see_own_team(self):
#         team_list = self.worker.my_team()
#     
# class Hr_interface:
#     def __init__(self,hr_employee):
#         self.hr = hr_employee
#
#     def show_menue(self):
#         while True:
#             op = int(input(f"""
#             Welcome {self.hr.name} .....
#                 Press the number in front of the option to perform an action :-
#                   1 : Open pending requests
#                   2 : Show all closed requests 
#                   3 : Exit 
#                   4 : 
#                   """)
#             )
#             if op == 1:
#                 self.open_pending_requests()
#             elif op == 2:
#                 self.show_closed_reqests()
#             elif op == 3:
#                 exit()
#             elif op == 4:
#                 pass
#             # elif op == 5:
#             #     self.testing_fn()
#     
#     def open_pending_requests(self):
#         requests = self.hr.pending_req
#         if not requests:
#             print("There are no pending requests")
#         else :
#             keys = ["request_id","created_by","assigned_hr","remark","update_commited_at","created_at",]
#             printable_requests = make_printable(keys,requests)
#             print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Remark","Commited At","Created At"]))
#
#             pending_req_ids = [ req[0] for req in printable_requests ]
#             while True:
#                 op = int(input("To approve a request press 1, to reject press 2 to go back to previous menue hit 0 \n"))
#                 if op == 1: 
#                     self.update_req_ui("approve",pending_req_ids)
#                 elif op == 2:
#                     self.update_req_ui("reject",pending_req_ids)
#                 elif op == 0:
#                     self.show_menue()
#
#     def update_req_ui(self,type,pending_req_ids):
#         req_id = int(input((f"""To {type} a request please enter the request id and hit enter
#         """)))
#         if req_id in pending_req_ids:
#             remark = input("Please enter a remak for the request : ")
#             self.hr.update_request_status(req_id,remark,type)
#         else :
#             print("Request not found please try again")
#
#     def show_closed_reqests(self):
#         requests = self.hr.closed_req
#         if not requests:
#             print("There are no pending requests")
#         else:
#             keys = ["request_id","created_by","assigned_hr","remark","update_commited_at","created_at",]
#             printable_requests = make_printable(keys,requests)
#             print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Remark","Commited At","Created At"]))

class Auth_interface:
    def __init__(self):
        print("this is the auth interface")

    def get_credentials(self):
        empId = int(input("""Please enter your employee id : """))
        password = input("""Please enter your password: """)
        return (empId, password)

    def login(self):
        user_obj = None
        # print("hello")
        while not user_obj :
            empId, password = self.get_credentials()
            auth_obj = Auth(empId,password)
            user_obj = auth_obj.login()
        # print(user_obj)
        return user_obj 

