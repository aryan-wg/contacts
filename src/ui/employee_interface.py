from tabulate import tabulate
from ..utils.general_utils import make_printable,take_address_input
import json

class EmployeeInterface():
    def __init__(self,employee):
        self.employee = employee 

    def see_my_profile(self):
        profile_info = self.employee.get_profile_info()
        keys = ["name","phone","email","empId","address"]
        printable_data_list = make_printable(keys,[profile_info])
        # address_keys = ["city","street","state","postal_code","country"]
        address = json.loads(printable_data_list[0][-1])
        # print(type(address))
        str_address = ""
        for key,value in address.items():
            str_address+=f"{key} - {value} \n"

        printable_data_list[0][-1] = str_address
        print(tabulate(printable_data_list,headers=["Name","Phone Number","Email","Employee ID","Address"]))

        op = int(input("\nTo request for a change in information press 1, to go back press 0 : "))
        if op == 0:
            return 
        elif op == 1:
            self.update_info_ui()
        #keys = ["request_id","created_by","assigned_hr","update_commited_at","created_at"]
        # printable_requests = make_printable(keys,requests)
        # print(tabulate(printable_requests, headers=["Request Id","Created By","Assigned HR","Commited At","Created At"]))

        pass

    def update_info_ui(self):
        worker_dict ={}
        worker_dict["name"] = input("Enter worker name : ")
        worker_dict["phone"] = int(input("Enter worker's phone number : "))
        worker_dict["email"]  = input("Enter worker's email address : ")
        worker_dict["address"]= take_address_input()

        success = self.employee.request_self_info_change(json.dumps(worker_dict))
        if success:
            self.employee.see_my_profile()
        else :
            print("There has been some error in creating a request")
            self.employee.see_my_profile()

    def search_other_employee(self):
        name = input("Enter the name of user you want to search for : ")
        search_result = self.employee.search_other_employee(name)
        if not len(search_result):
            print("No such users found ")
        else:
            headers = ["Emp Id","Name", "Phone No", "Email"]
            print(tabulate(search_result, headers))


