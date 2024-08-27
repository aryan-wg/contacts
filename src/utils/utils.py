from ..database.db_setup import get_cursor, get_con

tables_scema_map = {
    "employees": "INSERT INTO employees VALUES(:name, :phone, :email, :address)"
}
cur = get_cursor()
con = get_con()


def write_to_table(table_name, data_obj):
    print(data_obj)
    print(cur.execute(tables_scema_map[table_name], data_obj))
    print(con.commit())
    # print(data_obj)


def read_from_table():
    cur.execute('select * from employees')
    print(cur.fetchall())
    # print(cur.fetchall())

