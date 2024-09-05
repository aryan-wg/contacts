from ..utils.general_utils import int_input
from ..auth import Auth
import maskpass


class Auth_interface:
    def get_credentials(self):
        while True:
            empId = int_input("""Please enter your employee id : """)
            password = maskpass.askpass("""Please enter your password: """)
            return (empId, password)

    def login(self):
        user_obj = None
        while not user_obj:
            empId, password = self.get_credentials()
            auth_obj = Auth(empId, password)
            user_obj = auth_obj.login()
        return user_obj
