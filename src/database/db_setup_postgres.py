# import psycopg2
import json
import asyncpg

async def get_con():
    try:
        return await asyncpg.connect(database="postgres", user="postgres", host="localhost", password="adminadmin")
    except Exception as err:
        raise Exception(err)
    finally:
        print("Get connection finished ")




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
