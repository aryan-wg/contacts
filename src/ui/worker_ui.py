from tabulate import tabulate
from ..utils.general_utils import int_input, make_printable, take_address_input
from .employee_interface import EmployeeInterface

from pprint import pprint


class Worker_interface(EmployeeInterface):
    def __init__(self, worker):
        super().__init__(worker)
        self.worker = worker

    def show_menue(self):
        op = int_input(f"""
        Welcome {self.employee.name} .....
            Press the number in front of the option to perform an action :-
              1 : See my profile 
              2 : Search an employee
              3 : See own team
              4 : Update password 
              5 : Exit
              """)
        if op == 1:
            self.see_my_profile()
            self.show_menue()
        elif op == 2:
            self.search_other_employee()
        elif op == 3:
            self.see_own_team_ui(self.employee.empId)
            self.show_menue()
        elif op == 4:
            self.update_password_ui()
        elif op == 5:
            exit()

    def see_own_team_ui(self, empId):
        op = int_input(
            """
            Press the number in front of the option to perform an action :-
                1 : See people up in hierarchy 
                2 : See pople lower in heirarchy 
                0 : go to previous menue 
                """
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
            print(
                f"\n{reports_to["employee"]["name"]} with employee id {empId} reports to {reports_to["reports_to"]["name"]} with employee Id {reports_to["reports_to"]["empId"]}"
            )
            op = int_input(
                f"\nTo see more information about {reports_to["reports_to"]["name"]} press 1 \n Or 0 to continue : "
            )
            if op == 1:
                print(f"""
                      Name : {reports_to["reports_to"]["name"]}
                      Email : {reports_to["reports_to"]["email"]}
                      Phone : {reports_to["reports_to"]["phone"]}
                      Employee Id : {reports_to["reports_to"]["empId"]}
                           """)
                print(f"Currently at user {reports_to["reports_to"]["name"]}\n")
                self.see_own_team_ui(reports_to["reports_to"]["empId"])

            elif op == 0:
                print(f"Currently at user {reports_to["reports_to"]["empId"]}\n")
                self.see_own_team_ui(reports_to["reports_to"]["empId"])

    def reported_by_ui(self, empId):
        reported_by_workers = self.worker.reported_by(empId)
        if reported_by_workers == None:
            print("\nThis employee is not reported to by anyone\n")
            self.see_own_team_ui(empId)
        for reported_by in reported_by_workers:
            print(
                f"\n{reported_by["employee"]["name"]} with employee id {reported_by["employee"]["empId"]} reports to {reported_by["reports_to"]["name"]} employee with Id {reported_by["reports_to"]["empId"]}"
            )
        op = int_input(
            "\nTo see more information about any of the employees press 1\n Or press 0 to continue : "
        )
        if op == 1:
            while True:
                input_empId = int_input(
                    "Enter the employee id of the person you want more information of : "
                )
                for reported_by in reported_by_workers:
                    if input_empId == reported_by["employee"]["empId"]:
                        print(f"""
                              Name : {reported_by["employee"]["name"]}
                              Email : {reported_by["employee"]["email"]}
                              Phone : {reported_by["employee"]["phone"]}
                              Employee Id : {reported_by["employee"]["empId"]}
                                   """)
                        self.see_own_team_ui(input_empId)
                        break
                else:
                    print("Invalid employee id enterd ")
                    self.see_own_team_ui(empId)
        elif op == 0:
            self.see_own_team_ui(empId)
