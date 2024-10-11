# from src.database.db_setup_postgres import create_tables
from src.utils.async_pg_db_utils import (
    delete_from_table,
    write_to_table,
    read_fields_from_record,
    check_if_exists_in_db,
    match_string_in_field,
    read_by_multiple_attributes,
    read_by_multiple_att_and_keys,
    update_one_record,
)
import time
import asyncio


async def test_database_functionality():
    user_info = {
        "name": "ak",
        "phone": 9999999999,
        "email": "ak@k",
        "address": '{"street": "21", "postal_code": "2000", "city": "sre", "state": "up", "country": "ind"}',
        "password": "fsafjkldsjflksajfklsajfsfjlksajflksjfkaljflkdsaj",
        "user_type": "worker",
    }
    wtt = await write_to_table("employees", user_info)
    print("wtt ", wtt, "\n")

    time.sleep(2)
    rffr = await read_fields_from_record("employees", "name, user_type", "email", ["ak@k"])
    print("rffr ", rffr, "\n")

    time.sleep(2)
    cix0 = await check_if_exists_in_db("employees", "name", "pk")
    cix1 = await check_if_exists_in_db("employees", "name", "ak")
    print("cix1 ", cix1, cix0, "\n")

    time.sleep(2)
    msif = await match_string_in_field("employees", "name,email,phone", "email", "ak")
    print("msif ", msif)

    time.sleep(2)
    rbma = await read_by_multiple_attributes(
        "employees", "name,phone", ["name", "email"], ["ak", "ak@k"]
    )
    print("rmba ", rbma)

    time.sleep(2)
    user_info_2 = {
        "name": "pk",
        "phone": 9999999999,
        "email": "pkkkk@k",
        "address": '{"street": "21", "postal_code": "2000", "city": "sre", "state": "up", "country": "ind"}',
        "password": "fsafjkldsjflksajfklsajfsfjlksajflksjfkaljflkdsaj",
        "user_type": "worker",
    }
    await write_to_table("employees", user_info_2)

    time.sleep(2)
    rbmak = await read_by_multiple_att_and_keys(
        "employees", "name,email", ["name", "email"], ["ak", ["ak@k", "pkkkk@k"]]
    )
    print("rbmak ", rbmak)

    time.sleep(2)
    uor = await update_one_record("employees", user_info_2, "name", "ak")
    print("uor ", uor)

    time.sleep(2)
    dor = await delete_from_table("employees", "email", "pkkkk@k")
    print("dor ", dor)


asyncio.run(test_database_functionality())
