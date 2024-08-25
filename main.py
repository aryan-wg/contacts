from src.entities.admin.admin import Admin
def main():
    while True:
        user_name = input("Enter your employee Id :\n")
        password = input("Enter your password :\n")

        # op = input(f"""
        #            Welcome {name} to the contacts manager
        #            Select the operation you want to perfom (press corresponding key and hit enter)  
        #             - 
        #            """)
    name = "aryan"
    phone = "984783723"
    email = "aryan@gmail.com"
    address = {"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"}

    new_admin = Admin(name,phone,email,address)


    new_worker = new_admin.create_worker("employeeId1",["employeeId2"],("kamboj","4892348920","ak@gmail.com",{"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"})) 


    pending_requests= []
    closed_requests = []
    new_hr_manager = new_admin.create_hr_emp(pending_requests,closed_requests,("reportin_to_empID",["reported_by_empIDs"],("name","phone number must be int","email@email.com",{"street":"Delhi road","city":"gr noida","state":"Up","postal code":201306,"country":"IND"})))
    
if __name__ == "__main__":
    main()


