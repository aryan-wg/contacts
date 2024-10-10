# from sqlite3 import Cursor
from ..database.db_setup_postgres import get_con
from functools import reduce
from pprint import pprint
import time
# tables_insert_map = {
#     "employees": "INSERT INTO employees (name,phone,email,address,password,user_type) VALUES (:name,:phone,:email,:address,:password,:user_type) RETURNING *",
#     "requests": "INSERT INTO requests (created_by,updated_info,assigned_hr,created_at,update_committed_at,request_status) VALUES (:created_by,:updated_info,:assigned_hr,:created_at,:update_committed_at,:request_status) RETURNING *",
#     "relations": "INSERT INTO relations (employee , reports_to ) VALUES (:employee,:reports_to) RETURNING *",
# }

async def create_tables():
    con = await get_con()
    table_creation_queries = [
        """CREATE TABLE IF NOT EXISTS employees(

            empId SERIAL,
            name text NOT NULL,
            phone BIGINT NOT NULL,
            email text NOT NULL,
            address text NOT NULL,
            password text NOT NULL,
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
        await con.execute(query)


postgres_tables_insert_map = {
    "employees": """
        INSERT INTO employees (name, phone, email, address, password, user_type)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *
    """,
    "requests": """
        INSERT INTO requests (created_by, updated_info, assigned_hr, created_at, update_committed_at, request_status)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *
    """,
    "relations": """
        INSERT INTO relations (employee, reports_to)
        VALUES ($1,$2)
        RETURNING *
    """,
}
# %(created_by)s, %(updated_info)s, %(assigned_hr)s, %(created_at)s, %(update_committed_at)s, %(request_status)s
# %(employee)s, %(reports_to)s


async def delete_from_table(table, key_type, key):
    try:
        con = await get_con()
        if isinstance(key, str):
            con.execute(f"DELETE FROM {table} WHERE {key_type} = '{key}' ")
        else:
            con.execute(f"DELETE FROM {table} WHERE {key_type} = {key} ")
        con.commit()
        return True
    except Exception as err:
        print(err)
        return False


async def write_to_table(table, data_obj):
    values = None
    con = await get_con()
    match table:
        case "employee":
            values = (data_obj["name"],data_obj["phone"],data_obj["email"],data_obj["address"],data_obj["password"],data_obj["user_type"],)
        case "requests":
            values = (data_obj["created_by"],data_obj["updated_info"],data_obj["assigned_hr"],data_obj["created_at"],data_obj["update_committed_at"],data_obj["request_status"],)
        case "relations":
            values = (data_obj["employee"],data_obj["reports_to"])
        case _:
            raise ValueError(f"The schema of table {table} is not supported by write_to_table_method")

    returned = await con.execute(postgres_tables_insert_map[table], *values)
    return returned


async def read_fields_from_record(table, fields, key_type, keys):
    con = await get_con()
    data = []
    for key in keys:
        if isinstance(key, str):
            print(f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'")
            con.execute(f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'")
        else:
            con.execute(f"SELECT {fields} FROM {table} WHERE {key_type} = {key}")
        received = con.fetchall()
        for data_item in received:
            data.append(data_item)
    if len(data) >= 1:
        return data
    else:
        return []


async def check_if_exists_in_db(table, key_type, key):
    con = await get_con()
    con.execute(f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {key_type} = '{key}' )")
    (check,) = con.fetchone()
    return check


# def read_all_WHERE(table,fields,key_type,key):


async def match_string_in_field(table, get_fields_str, field, match):
    con = await get_con()
    query_string = f"SELECT {get_fields_str} FROM {table} WHERE {field} LIKE '{match}%'"
    con.execute(query_string)
    data = con.fetchmany(10)
    # print(data)
    return data


async def read_by_multiple_attributes(table, fields, key_types, keys):
    con = await get_con()
    where_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    for i in range(len(key_types)):
        where_query_str += f" {key_types[i]} = %({key_types[i]})s"

        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    # print(complete_query)
    con.execute(complete_query, key_value_dict)
    data = con.fetchall()
    return data


async def read_by_multiple_att_and_keys(table, fields, key_types, keys):
    con = await get_con()
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
    con.execute(complete_query, key_value_dict)
    data = con.fetchall()
    return data


async def update_one_record(table, values_dict, key_type, key):
    con = await get_con()
    set_string = ""
    argument_dict = {key_type: key}
    for key, value in values_dict.items():
        set_string += f" {key} = %({key})s,"

        argument_dict[f"{key}"] = value

    set_string = set_string[0:-1]
    query_string = f"update {table} set{set_string} WHERE {key_type} = %({key_type})s"
    con.execute(query_string, argument_dict)
    con.commit()
    return True


# def read_one_FROM_table(table,field,key_type,key):
#     con.execute(f"SELECT {field} FROM {table} WHERE {key_type}='{key}'")
#     item, = con.fetchone()
#     return item


def read_entire_table(table):
    con.execute(f"SELECT * FROM {table}")
    # print(con.fetchall())
    # print(con.fetchall())
