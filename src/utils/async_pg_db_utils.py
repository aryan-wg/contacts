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
        await con.fetchrow(query)


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
            await con.fetchrow(f"DELETE FROM {table} WHERE {key_type} = '{key}' ")
        else:
            await con.fetchrow(f"DELETE FROM {table} WHERE {key_type} = {key} ")
        return True
    except Exception as err:
        print(err)
        return False


async def write_to_table(table, data_obj):
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

    returned = dict(await con.fetchrow(postgres_tables_insert_map[table], *values))
    return returned


async def read_fields_from_record(table, fields, key_type, keys):
    con = await get_con()
    data = []
    for key in keys:
        received = None
        if isinstance(key, str):
            # print(f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'")
            received = dict(await con.fetchrow(
                f"SELECT {fields} FROM {table} WHERE {key_type}='{key}'"
            ))
        else:
            received = dict(await con.fetchrow(
                f"SELECT {fields} FROM {table} WHERE {key_type} = {key}"
            ))
        if isinstance(received, list):
            for data_item in received:
                data.append(data_item)
        elif received is not None:
            data.append(received)
    if len(data) >= 1:
        return data
    else:
        return []


async def check_if_exists_in_db(table, key_type, key):
    con = await get_con()
    check = dict(await con.fetchrow(
        f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {key_type} = '{key}' )"
    ))
    return check


# def read_all_WHERE(table,fields,key_type,key):


async def match_string_in_field(table, get_fields_str, field, match):
    con = await get_con()
    query_string = (
        f"SELECT {get_fields_str} FROM {table} WHERE {field} LIKE '{match}%' LIMIT 10"
    )
    data = dict(await con.fetchrow(query_string))
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
        query_tuple+=(key_value_dict[key_types[i]],)
        query_tuple_counter+=1
        if not i == len(keys) - 1:
            where_query_str += " and"

    complete_query = f"SELECT {fields} FROM {table} WHERE {where_query_str}"
    print(complete_query)
    data = dict(await con.fetchrow(complete_query,*query_tuple))
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
    data = dict(await con.fetchrow(complete_query,*query_tuple ))
    return data


async def update_one_record(table, values_dict, key_type, key):
    con = await get_con()
    set_string = ""
    query_tuple_counter = 1
    query_tuple = ()
    for key, value in values_dict.items():
        set_string += f" {key} = ${query_tuple_counter},"
        query_tuple_counter+=1
        query_tuple+=(value,)

    set_string = set_string[0:-1]
    query_string = f"update {table} set{set_string} WHERE {key_type} = {key} "
    await con.fetchrow(query_string, *query_tuple)
    return True


# def read_one_FROM_table(table,field,key_type,key):
#     con.fetchrow(f"SELECT {field} FROM {table} WHERE {key_type}='{key}'")
#     item, = con.fetchone()
#     return item


def read_entire_table(table):
    con.fetchrow(f"SELECT * FROM {table}")
    # print(con.fetchall())
    # print(con.fetchall())
