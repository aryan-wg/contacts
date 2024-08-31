import sqlite3
import json

con = sqlite3.connect("data.db")
cur = con.cursor()


def get_cursor():
    return cur


def get_con():
    return con


def create_tables():
    table_creation_queries = [
        """CREATE TABLE IF NOT EXISTS employees(

            empId integer primary key AUTOINCREMENT,
            name text NOT NULL,
            phone integer NOT NULL,
            email text NOT NULL,
            address text NOT NULL,
            password text NOT NULL,
            user_type text NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS relations(

            reports_to integer,
            employee integer, 
            team text)""",
        """CREATE TABLE IF NOT EXISTS requests(

            request_id integer primary key AUTOINCREMENT,
            created_by integer NOT NULL,
            updated_info text NOT NULL,
            assigned_hr integer,
            remark text,
            created_at integer NOT NULL,
            update_commited_at integer NOT NULL,
            request_status text NOT NULL)""",
    ]

    for query in table_creation_queries:
        cur.execute(query)

    con.commit()


changed_values_dict = {
    "name": "Akamboj",
    "phone": 12394823790,
    "email": "aryan@wg.com",
    "address": {
        "city": "noida",
        "street": "dl rd",
        "state": "uttar pradesh",
        "postal_code": 206301,
        "country": "India",
    }
}

string = json.dumps(changed_values_dict)

sample_data = [
    "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES ('Aryan',1234567890,'aryan@gmail.com','address_string','$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe','admin')",
    "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES ('shruti',99999999999,'shruti@gmail.com','shruti_address_string','$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe','hr')",
    "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES ('dev',8888888888,'dev@gmail.com','dev_address_string','$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe','worker')",
    f"INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_commited_at,request_status) VALUES (1,'{string}',2,1724941498,0,'approved_by_hr')",
    "INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_commited_at,request_status) VALUES (2,'shruti_updated_info',2,1724921498,0,'hr_not_assigned')",
    "INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_commited_at,request_status) VALUES (3,'dev_updated_info',2,1724951498,0,'rejected')",
    "INSERT INTO relations (reports_to , employee , team ) VALUES (0,1,'devs')",
    "INSERT INTO relations (reports_to , employee , team ) VALUES (1,2,'devs')",
    "INSERT INTO relations (reports_to , employee , team ) VALUES (1,3,'devs')",
    "INSERT INTO relations (reports_to , employee , team ) VALUES (2,3,'devs')",
]


def insert_sample_data():
    for sample_query in sample_data:
        cur.execute(sample_query)
    con.commit()


# def create_db_entry():
#     pass
