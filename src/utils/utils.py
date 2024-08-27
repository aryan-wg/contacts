from ..database.db_setup import get_cursor, get_con

# "CREATE TABLE IF NOT EXISTS relation(reports_to integer, reported_by integer, team text)"
tables_insert_map = {
    "employees": "INSERT INTO employees (name,phone,email,address) VALUES (:name,:phone,:email,:address)",
    "requests": "INSERT INTO requests (created_by,updated_info,approved_by_hr,created_at,update_commited) VALUES (:created_by,:updated_info,:approved_by_hr,:created_at,:update_commited)",
    "relations": "INSERT INTO relation (reports_to , reported_by , team ) VALUES (:reports_to,:reported_by,:team)",
}
cur = get_cursor()
con = get_con()


def write_to_table(table_name, data_obj):
    print(data_obj)
    print(cur.execute(tables_insert_map[table_name], data_obj))
    print(con.commit())


def read_from_table(table):
    cur.execute(f"select * from {table}")
    print(cur.fetchall())
    # print(cur.fetchall())
