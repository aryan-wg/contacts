import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()

def create_tables():
    cur.execute(
        "CREATE TABLE employees(empId integer NOT NULL, name text NOT NULL, phone integer NOT NULL, email text NOT NULL, address text NOT NULL)"
    )
    con.commit()

def create_db_entry():
    pass

