from src.database.db_setup import create_tables
from src.entities.admin.admin import Admin
from src.utils.utils import read_from_table, write_to_table


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

    name = "aryan"
    phone = "984783723"
    email = "aryan@gmail.com"
    address = {
        "street": "Delhi road",
        "city": "gr noida",
        "state": "Up",
        "postal code": 201306,
        "country": "IND",
    }

    new_admin = Admin(name, phone, email, address)

    # "empId": 31237891,
    new_person_data = {
        "empId":None,
        "name": "",
        "phone": 718937819,
        "email": "this is email",
        "address": "something",
    }
    create_tables()

    write_to_table("employees", new_person_data)
    read_from_table("employees")
    new_worker = new_admin.create_worker(
        "employeeId1",
        ["employeeId2"],
        (
            "kamboj",
            "4892348920",
            "ak@gmail.com",
            {
                "street": "Delhi road",
                "city": "gr noida",
                "state": "Up",
                "postal code": 201306,
                "country": "IND",
            },
        ),
    )

    personal_info = (
        "name",
        "phone number must be int",
        "email@email.com",
        {
            "street": "Delhi road",
            "city": "gr noida",
            "state": "Up",
            "postal code": 201306,
            "country": "IND",
        },
    )

    worker_info = (
        ("reportin_to_empID", ["reported_by_empIDs"], personal_info),)

    hr_emp_info = worker_info

    new_hr_employee = new_admin.create_hr_emp(hr_emp_info)


if __name__ == "__main__":
    main()
