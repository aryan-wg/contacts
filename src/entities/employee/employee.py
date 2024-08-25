from abc import ABC,abstractmethod

class Employee(ABC):
    def __init__(self,*args):
        name,phone,email,address = args 

        self.name = name
        self.phone = phone
        self.email = email

        # this address will be a dict that has information 
        # street,city,state,postal code, country

        self.address = address
        print("new employee instantiated ",self.name) 
        # print(self.name,self.phone,self.email,self.address)        

    def search_other_employee(name):
        print("searchin for",name)

    def request_self_info_change(updated_user):
        print("updated user will be ",updated_user)
    @abstractmethod 
    def info():
        pass
# print("employee")

# name = "aryan"
# phone = "984783723"
# email = "aryan@gmail.com"
# address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}
# new_emp = employee(name,phone,email,address)


