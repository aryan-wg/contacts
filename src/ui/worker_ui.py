from tabulate import tabulate
from ..utils.general_utils import make_printable, take_address_input
from .employee_interface import EmployeeInterface

from pprint import pprint

import json


class Worker_interface(EmployeeInterface):
    def __init__(self, worker):
        super().__init__(worker)
        self.worker = worker

    def show_menue(self):
        op = int(
            input(f"""
        Welcome {self.employee.name} .....
            Press the number in front of the option to perform an action :-
              1 : See my profile 
              2 : Search an employee
              3 : See own team
              4 : Exit
              """)
        )
        if op == 1:
            self.see_my_profile()
            self.show_menue()
        elif op == 2:
            self.search_other_employee()
        elif op == 3:
            self.see_own_team_ui(self.employee.empId)
            self.show_menue()
        elif op == 4:
            exit()

    def see_own_team_ui(self,empId):
        op = int(
            input(
                "1 : To see people up in hierarchy \n2 : To see pople lower in heirarchy \n0 : To go back to previous menue \n"
            )
        )
        if op == 1:
            self.reports_to_ui(empId)
        elif op == 2:
            self.reported_by_ui(empId)
        elif op == 0:
            self.show_menue()

    def reports_to_ui(self, empId):
        reports_to = self.worker.reports_to(empId)

        if reports_to["reports_to"]["name"] == None:
            print("\nThis employee does not report to anyone \n")
            self.see_own_team_ui(empId)
        else:
            print(f"\n{reports_to["employee"]["name"]} with employee id {empId} reports to {reports_to["reports_to"]["name"]} employee with Id {reports_to["reports_to"]["empId"]}")
            op = int(input(f"\nTo see more information about {reports_to["reports_to"]["name"]} press 1 , 0 to continue "))
            if op == 1:
                print(f"""
                      Name : {reports_to["reports_to"]["name"]}
                      Email : {reports_to["reports_to"]["email"]}
                      Phone : {reports_to["reports_to"]["phone"]}
                      Employee Id : {reports_to["reports_to"]["phone"]}
                           """)
                print(f"Currently at user {reports_to["reports_to"]["name"]}\n")
                self.see_own_team_ui(reports_to["reports_to"]["empId"])

            elif op == 0:
                print(f"Currently at user {reports_to["reports_to"]["empId"]}\n")
                self.see_own_team_ui(reports_to["reports_to"]["empId"])

    def reported_by_ui(self, empId):
        reported_by = self.worker.reported_by(empId)

        print(f"{reported_by["employee"]["name"]} with employee id {empId} reports to employee with Id {reports_to["reports_to"]["empId"]} name {reports_to["reports_to"]["name"]}")
        op = int(input(f"To see more information about {reported_by["reports_to"]["name"]} press 1 , 0 to continue "))
        if op == 1:
            print(f"""
                  Name : {reported_by["reports_to"]["name"]}
                  Email : {reported_by["reports_to"]["email"]}
                  Phone : {reported_by["reports_to"]["phone"]}
                  Employee Id : {reported_by["reports_to"]["phone"]}
                       """)
            self.see_own_team_ui(reported_by["empId"])

        elif op == 0:
            self.see_own_team_ui(reported_by["empId"])


        self.see_own_team_ui(reported_by["empId"])
