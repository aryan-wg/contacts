# from sqlite3 import Cursor
from ..database.db_setup_postgres import get_cursor, get_con
from functools import reduce
from pprint import pprint

# tables_insert_map = {
#     "employees": "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (:name,:phone,:email,:address,:password,:user_type) RETURNING *",
#     "requests": "INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_committed_at,request_status) VALUES (:created_by,:updated_info,:assigned_hr,:created_at,:update_committed_at,:request_status) RETURNING *",
#     "relations": "INSERT INTO relations (employee , reports_to ) VALUES (:employee,:reports_to) RETURNING *",
# }
postgres_tables_insert_map = {
    "employees": """
        INSERT INTO employees (name, phone, email, address, password, user_type)
        VALUES (%(name)s, %(phone)s, %(email)s, %(address)s, %(password)s, %(user_type)s)
        RETURNING *
    """,
    "requests": """
        INSERT INTO requests (created_by, updated_info, assigned_hr, created_at, update_committed_at, request_status)
        VALUES (%(created_by)s, %(updated_info)s, %(assigned_hr)s, %(created_at)s, %(update_committed_at)s, %(request_status)s)
        RETURNING *
    """,
    "relations": """
        INSERT INTO relations (employee, reports_to)
        VALUES (%(employee)s, %(reports_to)s)
        RETURNING *
    """,
}
cur = get_cursor()
con = get_con()


def delete_from_table(table, key_type, key):
    try:
        if isinstance(key, str):
            cur.execute(f"DELETE FROM {table} WHERE {key_type} = '{key}' ")
        else:
            cur.execute(f"DELETE FROM {table} WHERE {key_type} = {key} ")
        con.commit()
        return True
    except Exception as err:
        print(err)
        return False


def write_to_table(table, data_obj):
    cur.execute(postgres_tables_insert_map[table], data_obj)
    returned = cur.fetchone()
    con.commit()
    return returned


def read_fields_from_record(table, fields, key_type, keys):
    data = []
    for key in keys:
        if isinstance(key, str):
            print(f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'")
            cur.execute(f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'")
        else:
            cur.execute(f"SELECT {fields} FROM {table} WHERE {key_type} = {key}")
        received = cur.fetchall()
        for data_item in received:
            data.append(data_item)
    if len(data) >= 1:
        return data
    else:
        return []


def check_if_exists_in_db(table, key_type, key):
    cur.execute(f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {key_type} = '{key}' )")
    (check,) = cur.fetchone()
    return check


# def read_all_WHERE(table,fields,key_type,key):


def match_string_in_field(table, get_fields_str, field, match):
    query_string = f"SELECT {get_fields_str} FROM {table} WHERE {field} LIKE '{match}%'"
    cur.execute(query_string)
    data = cur.fetchmany(10)
    # print(data)
    return data


def read_by_multiple_attributes(table, fields, key_types, keys):
    where_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    for i in range(len(key_types)):
        where_query_str += f" {key_types[i]} = %({key_types[i]})s"

        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    # print(complete_query)
    cur.execute(complete_query, key_value_dict)
    data = cur.fetchall()
    return data


def read_by_multiple_att_and_keys(table, fields, key_types, keys):
    where_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    for i in range(len(key_types)):
        if isinstance(keys[i], list):
            possible_values = reduce(lambda x, y: f"{x}" + " " + f"'{y}',", keys[i], "")

            possible_values = possible_values[0:-1]  # removing the extra " , " FROM end
            # print(possible_values)
            where_query_str += f" {key_types[i]} IN ({possible_values})"
        else:
            where_query_str += f" {key_types[i]} = %({key_types[i]})s"

        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    cur.execute(complete_query, key_value_dict)
    data = cur.fetchall()
    return data


def update_one_record(table, values_dict, key_type, key):
    set_string = ""
    argument_dict = {key_type: key}
    for key, value in values_dict.items():
        set_string += f" {key} = %({key})s,"

        argument_dict[f"{key}"] = value

    set_string = set_string[0:-1]
    query_string = f"update {table} set{set_string} WHERE {key_type} = %({key_type})s"
    cur.execute(query_string, argument_dict)
    con.commit()
    return True


# def read_one_FROM_table(table,field,key_type,key):
#     cur.execute(f"SELECT {field} FROM {table} WHERE {key_type}='{key}'")
#     item, = cur.fetchone()
#     return item


def read_entire_table(table):
    cur.execute(f"SELECT * FROM {table}")
    # print(cur.fetchall())
    # print(cur.fetchall())
