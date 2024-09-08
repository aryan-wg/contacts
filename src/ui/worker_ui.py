from tabulate import tabulate
from ..utils.general_utils import print_relation,format_for_display, get_address_input, print_user_info_in_relation
from ..utils.validations_utils import int_input
from .employee_ui import EmployeeUi

from pprint import pprint


class WorkerUi(EmployeeUi):
    def __init__(self, worker):
        super().__init__(worker)
        self.worker = worker

    def show_menu(self):
        selected = int_input(f"""
----------------------------------------------------------------------------------------------
Welcome {self.employee.name} .....
Press the number in front of the selectedtion to perform an action :-
1 : See my profile 
2 : Search an employee
3 : See my team
4 : Update password 
5 : Exit
----------------------------------------------------------------------------------------------
""")
        match selected:
            case 1:
                self.see_my_profile()
            case 2:
                self.search_other_employee()
            case 3:
                self.show_my_team(self.employee.empId)
            case 4:
                self.update_password_input()
            case 5:
                exit()

    def show_my_team(self, empId):
        selected = int_input(
            """
----------------------------------------------------------------------------------------------
Press the number in front of the selectedtion to perform an action :-
1 : See people up in hierarchy 
2 : See people lower in hierarchy 
0 : go to previous menu 
----------------------------------------------------------------------------------------------
                """
        )
        match selected:
            case 1:
                self.user_reports_to(empId)
            case 2:
                self.user_reported_by(empId)
            case 0:
               return  

    def user_reports_to(self, empId):
        reports_to = self.worker.reports_to(empId)

        if reports_to["reports_to"]["name"] is None:
            print("\nThis employee does not report to anyone \n")
            self.show_my_team(empId)
        else:
            print_relation(reports_to)
            selected = int_input(
                f"\nTo see more information about {reports_to["reports_to"]["name"]} press 1\nOr 0 to continue : "
            )
            if selected == 1:
                print_user_info_in_relation(reports_to,"reports_to")
                print(f"Currently at user {reports_to["reports_to"]["name"]}\n")
                self.show_my_team(reports_to["reports_to"]["empId"])

            elif selected == 0:
                print(f"Currently at user {reports_to["reports_to"]["empId"]}\n")
                self.show_my_team(reports_to["reports_to"]["empId"])

    def user_reported_by(self, empId):
        reported_by_workers = self.worker.reported_by(empId)

        if reported_by_workers is None:
            print("\nThis employee is not reported to by anyone\n")
            self.show_my_team(empId)

        for reported_by in reported_by_workers:
            print_relation(reported_by)

        selected = int_input(
            "\nTo see more information about any of the employees press 1\n Or press 0 to continue : "
        )
        if selected == 1:
            while True:
                input_empId = int_input(
                    "\nEnter the employee id of the person you want more information of : "
                )
                for relation in reported_by_workers:
                    if input_empId == relation["employee"]["empId"]:
                        print_user_info_in_relation(relation,"employee")
                        self.show_my_team(input_empId)
                        break
                else:
                    print("Invalid employee id entered ")
                    self.show_my_team(empId)
        elif selected == 0:
            self.show_my_team(empId)
