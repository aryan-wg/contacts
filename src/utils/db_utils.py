from ..database.db_setup import get_cursor, get_con
from functools import reduce

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


def read_fields_from_record(table, fields, key_type, keys):
    for key in keys:
        if isinstance(key, str):
            cur.execute(f"select {fields} from {table} where {key_type}='{key}'")
        else:
            cur.execute(f"select {fields} from {table} where {key_type} = {key}")

    data = cur.fetchall()
    # print(data)

    if len(data) > 1:
        return data
    elif len(data) == 1:
        return [data[0]]
    else:
        return None

# def read_all_where(table,fields,key_type,key):


def read_by_multiple_attributes(table, fields, key_types, keys):
    WHERE_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    for i in range(len(key_types)):
        WHERE_query_str += f" {key_types[i]} = :{key_types[i]}"

        if not i == len(keys) - 1:
            WHERE_query_str += " and"

    complete_query = f"select {fields} from {table} where {WHERE_query_str}"
    # print(complete_query)
    cur.execute(complete_query, key_value_dict)
    data = cur.fetchall()
    return data


def read_by_multiple_att_and_keys(table, fields, key_types, keys):
    WHERE_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    for i in range(len(key_types)):
        if isinstance(keys[i], list):
            possible_values = reduce(lambda x, y: f"{x}" + " " + f"'{y}',", keys[i], "")

            possible_values = possible_values[0:-1] #removing the extra " , " from end 
            # print(possible_values)
            WHERE_query_str += f" {key_types[i]} IN ({possible_values})"
        else:
            WHERE_query_str += f" {key_types[i]} = :{key_types[i]}"

        if not i == len(keys) - 1:
            WHERE_query_str += " and"

    complete_query = f"select {fields} from {table} where {WHERE_query_str}"
    cur.execute(complete_query, key_value_dict)
    data = cur.fetchall()
    return data


# def read_one_from_table(table,field,key_type,key):
#     cur.execute(f"select {field} from {table} where {key_type}='{key}'")
#     item, = cur.fetchone()
#     return item


def read_entire_table(table):
    cur.execute(f"select * from {table}")
    print(cur.fetchall())
    # print(cur.fetchall())
