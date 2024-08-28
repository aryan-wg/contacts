from src.database.db_setup import create_tables
from src.entities.admin.admin import Admin
from src.utils.utils import read_from_table, write_to_table
import bcrypt

def main():
    {
        # while True:
        # user_name = input("Enter your employee Id :\n")
        # password = input("Enter your password :\n")
        # op = input(f"""
        #            Welcome {name} to the contacts manager
        #            Select the operation you want to perfom (press corresponding key and hit enter)
        #             -
        #            """)
    }
    {
        # name = "aryan"
        # phone = "984783723"
        # email = "aryan@gmail.com"
        # address = {
        #     "street": "Delhi road",
        #     "city": "gr noida",
        #     "state": "Up",
        #     "postal code": 201306,
        #     "country": "IND",
        # }
        #
        # new_admin = Admin(name, phone, email, address)
        #
        # # "empId": 31237891,
        # new_worker = new_admin.create_worker(
        #     "employeeId1",
        #     ["employeeId2"],
        #     (
        #         "kamboj",
        #         "4892348920",
        #         "ak@gmail.com",
        #         {
        #             "street": "Delhi road",
        #             "city": "gr noida",
        #             "state": "Up",
        #             "postal code": 201306,
        #             "country": "IND",
        #         },
        #     ),
        # )
        #
        # personal_info = (
        #     "name",
        #     "phone number must be int",
        #     "email@email.com",
        #     {
        #         "street": "Delhi road",
        #         "city": "gr noida",
        #         "state": "Up",
        #         "postal code": 201306,
        #         "country": "IND",
        #     },
        # )
        #
        # worker_info = (
        #     ("reportin_to_empID", ["reported_by_empIDs"], personal_info),)
        #
        # hr_emp_info = worker_info
        #
        # new_hr_employee = new_admin.create_hr_emp(hr_emp_info)

        }

    create_tables()
    new_person_data = {
        "empId":None,
        "name": "yan",
        "phone": 718937819,
        "email": "this is email",
        "address": "something",
        "user_type":"admin"
    }
    password = new_person_data["name"]+str(new_person_data["phone"])
    password = password.encode()
    hashed_pass = bcrypt.hashpw(password,bcrypt.gensalt(12))
    # print(hashed_pass)
    new_person_data["password"]=hashed_pass

    write_to_table("employees", new_person_data)
    read_from_table("employees")

    # employees(empId integer primary key AUTOINCREMENT , name text NOT NULL, phone integer NOT NULL, email text NOT NULL, address text NOT NULL, password text NOT NULL, user_type text NOT NULL)"
    # relations(reports_to integer, reported_by integer, team text)"
    # requests(request_id integer primary key AUTOINCREMENT, created_by integer NOT NULL, updated_info text NOT NULL, hr_assigned integer, approved_by_hr integer NOT NULL, remark text, created_at integer NOT NULL, update_commited integer NOT NULL)"


if __name__ == "__main__":
    main()
