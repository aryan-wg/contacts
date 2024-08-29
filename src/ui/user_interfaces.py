from pprint import pprint
from ..auth import Auth

class Admin_interface:
    def __init__(self, admin):
        self.admin = admin

    def show_menue(self):
        op = int(input(f"""
        Welcome {self.admin.name} .....
            Press the number in front of the option to perform an action :-
              1 : Show pending requests
              2 : Create a new worker
              3 : Create a new HR employee
              4 : Show all commited requests
              """)
        )


    def show_all_requests(self):
        for request in self.admin.pending_requests:
            pprint(request)

        for request in self.admin.closed_requests:
            pprint(request)


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
