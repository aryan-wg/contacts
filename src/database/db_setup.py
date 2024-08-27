import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()

def get_cursor():
    return cur
def get_con():
    return con
def create_tables():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employees(empId integer default 1 primary key, name text NOT NULL, phone integer NOT NULL, email text NOT NULL, address text NOT NULL) WITHOUT ROWID"
    )
    con.commit()

# def create_db_entry():
#     pass

