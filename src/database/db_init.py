from .db_setup_postgres import get_con
from ..entities.admin.admin import Admin
from ..Logger.Logger import Logger

async def create_tables():
    con = await get_con()
    table_creation_queries = [
        """CREATE TABLE IF NOT EXISTS employees(

            empId SERIAL,
            name text NOT NULL,
            phone BIGINT NOT NULL,
            email text NOT NULL,
            address text NOT NULL,
            password bytea NOT NULL,
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
        await con.fetch(query)
    await create_first_admin()

async def create_first_admin():
    logger = Logger("logs.log","App just started")
    adminObj = Admin(0,logger)
    data = {
        "name": "Admin",
        "phone": 9999999999,
        "email": "admin@admin.com",
        "address": {
            "city": "admin",
            "street": "admin",
            "state": "admin",
            "postal_code": 000000,
            "country": "admin",
        },
        "user_type": "admin",
        "password": "admin",
    }
    try:
        print("create_first_admin")
        await adminObj.create_new_employee(data)
        return True
    except Exception as err:
        print("There was an error while creating the first admin user", str(err))
    finally:
        del adminObj
