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
            await con.fetch(f"DELETE FROM {table} WHERE {key_type} = '{key}' ")
        else:
            await con.fetch(f"DELETE FROM {table} WHERE {key_type} = {key} ")
        return True
    except Exception as err:
        print(err)
        return False


async def write_to_table(table, data_obj):
    try:
        values = None
        con = await get_con()
        match table:
            case "employees":
                values = (
                    data_obj["name"],
                    data_obj["phone"],
                    data_obj["email"],
                    data_obj["address"],
                    data_obj["password"],
                    data_obj["user_type"],
                )
            case "requests":
                values = (
                    data_obj["created_by"],
                    data_obj["updated_info"],
                    data_obj["assigned_hr"],
                    data_obj["created_at"],
                    data_obj["update_committed_at"],
                    data_obj["request_status"],
                )
            case "relations":
                values = (data_obj["employee"], data_obj["reports_to"])
            case _:
                raise ValueError(
                    f"The schema of table {table} is not supported by write_to_table_method"
                )

        returned = await con.fetch(postgres_tables_insert_map[table], *values)
        if returned:
            return tuple(dict(returned[0]).values())
        else:
            raise Exception("Could not write to table")
    except Exception as err:
        raise Exception(str(err))


async def read_fields_from_record(table, fields, key_type, keys):
    con = await get_con()
    # print("read_fields_from_record")
    # print(await con.fetch("SELECT * FROM employees"))
    data = []
    for key in keys:
        received = None
        if isinstance(key, str):
            received = await con.fetch(
                f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'"
            )
        else:
            received = await con.fetch(
                f"SELECT {fields} FROM {table} WHERE {key_type} = {key}"
            )
        if received is not None:
            if isinstance(received, list):
                for data_item in received:
                    data.append(tuple(dict(data_item).values()))
            else:
                data.append(tuple(dict(received).values()))
    if len(data) >= 1:
        return data
    else:
        return []


async def check_if_exists_in_db(table, key_type, key):
    con = await get_con()
    check = await con.fetch(
        f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {key_type} = '{key}' )"
    )
    if check:
        return check[0]["exists"]
    else:
        return False


# def read_all_WHERE(table,fields,key_type,key):


async def match_string_in_field(table, get_fields_str, field, match):
    con = await get_con()
    query_string = (
        f"SELECT {get_fields_str} FROM {table} WHERE {field} LIKE '{match}%' LIMIT 10"
    )
    data = dict(await con.fetch(query_string))
    # print(data)
    return data


async def read_by_multiple_attributes(table, fields, key_types, keys):
    con = await get_con()
    where_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}
    query_tuple = ()
    query_tuple_counter = 1
    for i in range(len(key_types)):
        where_query_str += f" {key_types[i]} = ${query_tuple_counter}"
        query_tuple += (key_value_dict[key_types[i]],)
        query_tuple_counter += 1
        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    print(complete_query)
    received = await con.fetch(complete_query, *query_tuple)
    data = []
    if received is not None:
        for item in received:
            data.append(tuple(dict(item)))
    return data


async def read_by_multiple_att_and_keys(table, fields, key_types, keys):
    con = await get_con()
    where_query_str = ""
    key_value_dict = {key_types[i]: keys[i] for i in range(len(key_types))}

    query_tuple_counter = 1
    query_tuple = ()
    for i in range(len(key_types)):
        if isinstance(keys[i], list):
            possible_values = reduce(lambda x, y: f"{x}" + " " + f"'{y}',", keys[i], "")

            possible_values = possible_values[0:-1]  # removing the extra " , " FROM end
            # print(possible_values)
            where_query_str += f" {key_types[i]} IN ({possible_values})"
        else:
            where_query_str += f" {key_types[i]} = ${query_tuple_counter}"
            query_tuple_counter += 1
            query_tuple += (key_value_dict[f"{key_types[i]}"],)

        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    print(complete_query)
    data = dict(await con.fetch(complete_query, *query_tuple))
    return data


async def update_one_record(table, values_dict, key_type, key):
    con = await get_con()
    set_string = ""
    query_tuple_counter = 1
    query_tuple = ()
    for key, value in values_dict.items():
        set_string += f" {key} = ${query_tuple_counter},"
        query_tuple_counter += 1
        query_tuple += (value,)

    set_string = set_string[0:-1]
    query_string = f"update {table} set{set_string} WHERE {key_type} = {key} "
    await con.fetch(query_string, *query_tuple)
    return True


# def read_one_FROM_table(table,field,key_type,key):
#     con.fetch(f"SELECT {field} FROM {table} WHERE {key_type}='{key}'")
#     item, = con.fetchone()
#     return item


def read_entire_table(table):
    con.fetch(f"SELECT * FROM {table}")
    # print(con.fetchall())
    # print(con.fetchall())
