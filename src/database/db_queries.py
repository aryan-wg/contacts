import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()


def get_cursor():
    return cur


def create_tables():
    cur.execute(
        "CREATE TABLE employees(empId integer AUTOINCREMENT NOT NULL, name text NOT NULL, phone integer NOT NULL, email text NOT NULL, address text NOT NULL)"
    )
    con.commit()


# def create_db_entry():
#     pass
