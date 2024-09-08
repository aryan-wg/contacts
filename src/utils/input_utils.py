from .validations_utils import validate_phone,validate_email,validate_password 

def phone_input(worker_dict):
    while True:
        worker_dict["phone"] = input(
            f"Enter {"your" if not worker_dict["user_type"] else worker_dict["user_type"]+"'s"} phone number : "
        )
        if validate_phone(worker_dict["phone"]):
           return worker_dict 
        else:
            print("Enter a valid phone number.")

def email_input(worker_dict):
    while True:
        worker_dict["email"] = input(
            f"Enter {"your" if not worker_dict["user_type"] else worker_dict["user_type"]+"'s"} email address : "
        )
        if validate_email(worker_dict["email"]):
            return worker_dict
        else:
            print("Enter a valid email.")

def password_input(worker_dict):
    while True:
        worker_dict["password"] = input(f"Enter {"your" if not worker_dict["user_type"] else worker_dict["user_type"]+"'s"} password \n(must be 8 char long and contain 1 digit, 1 lowercase, 1 uppercase, 1 special character) : ")

        if validate_password(worker_dict["password"]):
            return worker_dict
        else:
            print("Enter a valid password.")

