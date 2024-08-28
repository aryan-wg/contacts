from pprint import pprint
from ..auth import Auth

class Admin_interface:
    def __init__(self, admin):
        self.admin = admin
        print("this is the home interface")

    def show_menue(self):
        print("""this is the menue of admin""")

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
