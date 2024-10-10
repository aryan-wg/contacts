import psycopg2
import json

con = psycopg2.connect(
    dbname="postgres", user="postgres", host="localhost", password="adminadmin"
)
cur = con.cursor()


def get_cursor():
    return cur


def get_con():
    return con


def create_tables():
    table_creation_queries = [
        """CREATE TABLE IF NOT EXISTS employees(

            empId SERIAL,
            name text NOT NULL,
            phone BIGINT NOT NULL,
            email text NOT NULL,
            address text NOT NULL,
            password text NOT NULL,
            user_type text NOT NULL)""",
        """CREATE TABLE IF NOT EXISTS relations(

            reports_to integer,
            employee integer 
            )""",
        """CREATE TABLE IF NOT EXISTS requests(

            request_id SERIAL,
            created_by integer NOT NULL,
            updated_info text NOT NULL,
            assigned_hr integer,
            remark text,
            created_at bigint NOT NULL,
            update_committed_at bigint NOT NULL,
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
    },
}

string = json.dumps(changed_values_dict)
string = '{"name": "ak", "phone": 1, "email": "ak@k", "address": "{"street": "21", "postal_code": "2000", "city": "sre", "state": "up", "country": "ind"}"}'
sample_data = [
    'INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (\'Aryan\',1234567890,\'aryan@gmail.com\',\'{"street": "21", "postal_code": "2008", "city": "sre", "state": "ind", "country": "ind"}\',\'$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe\',\'admin\')',
    'INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (\'shruti\',99999999999,\'shruti@gmail.com\',\'{"street": "21", "postal_code": "2008", "city": "sre", "state": "ind", "country": "ind"}\',\'$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe\',\'hr\')',
    'INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (\'dev\',8888888888,\'dev@gmail.com\',\'{"street": "21", "postal_code": "2008", "city": "sre", "state": "ind", "country": "ind"}\',\'$2b$12$etdIcyequaX8BS.Xfof50.FX8AOHLFa8A6W/.Gb0iHATPRjZtsiXe\',\'worker\')',
    f"INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_committed_at,request_status) VALUES (1,'{string}',2,1724941498,0,'approved_by_hr')",
    f"INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_committed_at,request_status) VALUES (2,'{string}',2,1724921498,0,'hr_not_assigned')",
    f"INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_committed_at,request_status) VALUES (3,'{string}',2,1724951498,0,'rejected')",
    "INSERT INTO relations (reports_to , employee ) VALUES (0,1)",
    "INSERT INTO relations (reports_to , employee ) VALUES (1,2)",
    "INSERT INTO relations (reports_to , employee ) VALUES (1,3)",
    "INSERT INTO relations (reports_to , employee ) VALUES (2,3)",
]


def insert_sample_data():
    for sample_query in sample_data:
        cur.execute(sample_query)
    con.commit()


# def create_db_entry():
#     pass
