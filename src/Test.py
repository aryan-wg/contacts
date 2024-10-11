from .utils.async_pg_db_utils import write_to_table

counter = 0
class Test():
    async def sqlite_multiple_read_write_calls(self):
        try:
            # obj = await write_to_table("relations",{"reports_to":999,"employee":999})
            global counter
            counter+=1
            obj = counter
            return obj
        except Exception as err:
            return f"ERROR.............{str(err)}"
