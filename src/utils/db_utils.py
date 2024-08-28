from ..database.db_setup import get_cursor, get_con

tables_insert_map = {
    "employees": "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (:name,:phone,:email,:address,:password,:user_type)",
    "requests": "INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_commited_at,request_status) VALUES (:created_by,:updated_info,:assigned_hr,:created_at,:update_commited_at,:request_status)",
    "relations": "INSERT INTO relations (reports_to , reported_by , team ) VALUES (:reports_to,:reported_by,:team)",
}
cur = get_cursor()
con = get_con()


def write_to_table(table, data_obj):
    print(cur.execute(tables_insert_map[table], data_obj))
    print(con.commit())

def read_fields_from_record(table,fields,key_type,keys):
    for key in keys:
        cur.execute(f"select {fields} from {table} where {key_type}='{key}'")

    data = cur.fetchall()

    # print(data)

    if len(data)>1:
        return data
    elif len(data) == 1:
        return [data[0]]
    else:
        return None 

# def read_one_from_table(table,field,key_type,key):
#     cur.execute(f"select {field} from {table} where {key_type}='{key}'")
#     item, = cur.fetchone()
#     return item

def read_entire_table(table):
    cur.execute(f"select * from {table}")
    print(cur.fetchall())
    # print(cur.fetchall())
