import sqlite3

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
            reported_by integer, 
            team text)""",

        """CREATE TABLE IF NOT EXISTS requests(

            request_id integer primary key AUTOINCREMENT,
            created_by integer NOT NULL,
            updated_info text NOT NULL,
            hr_assigned integer,
            approved_by_hr integer NOT NULL,
            remark text,
            created_at integer NOT NULL,
            update_commited integer NOT NULL)"""
    ]
    for query in table_creation_queries:
        cur.execute(query)

    con.commit()


# def create_db_entry():
#     pass
