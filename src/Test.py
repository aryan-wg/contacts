from .utils.db_utils import write_to_table

class Test():
    def sqlite_multiple_read_write_calls(self):
        try:
            obj = write_to_table("relations",{"reports_to":999,"employee":999})
            return obj
        except Exception as err:
            return f"ERROR.............{str(err)}"
