from tabulate import tabulate
from ..utils.general_utils import make_printable,take_address_input
from employee_interface import EmployeeInterface

import json
class Worker_interface(EmployeeInterface):
    def __init__(self,employee):
        super.__init__(employee) 

    def show_menue(self):
        op = int(input(f"""
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
            self.see_own_team()
            self.show_menue()
        elif op == 4:
            exit()

    def see_own_team(self):
        # team_list = self.my_team()
        print("not implemented")
