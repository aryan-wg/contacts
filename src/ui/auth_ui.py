from ..auth import Auth
import maskpass
class Auth_interface:
    # def __init__(self):
        # print("this is the auth interface")

    def get_credentials(self):
        empId = int(input("""Please enter your employee id : """))
        password = maskpass.askpass("""Please enter your password: """)
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

