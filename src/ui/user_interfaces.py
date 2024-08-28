from pprint import pprint

class Admin_interface:
    def __init__(self,admin):
        self.admin = admin
        print("this is the home interface")

    def show_all_requests(self):
        for request in self.admin.pending_requests:
            pprint(request)

        for request in self.admin.closed_requests:
            pprint(request)

class Auth_interface:
    def __init__(self):
        print("this is the auth interface")

    def get_login(self):
        empId = int(input("""Please enter your employee id : """))
        password = input("""Please enter your password: """)
        return (empId, password)
