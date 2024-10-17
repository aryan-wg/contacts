from ..employee.employee import Employee
from ...utils.async_pg_db_utils import check_if_exists_in_db, read_fields_from_record
from ...utils.parsing_populating_utils import parse_relations, populate_relations

from pprint import pprint


class Worker(Employee):
    # def __init__(self, employee_info):
    #     if len(employee_info) == 5:
    #         super().__init__((*employee_info, "worker"))
    #     elif len(employee_info) == 6:
    #         super().__init__(employee_info)

    def __init__(self, emp_id,logger):
        super().__init__(emp_id,logger)

    async def get_reports_to(self, emp_id):
        if not await check_if_exists_in_db("employees","empId",emp_id):
            raise ValueError("Employee does not exist.")
        else :
            data = await read_fields_from_record("relations", "*", "employee", [emp_id])
            if data[0][0]:
                data = parse_relations(data)
                data = await populate_relations(data)
                return data[0]
            else:
                return [] 

    async def get_reported_by(self, emp_id):
        if not await check_if_exists_in_db("employees","empId",emp_id):
            raise ValueError("Employee does not exist.")
        else:
            data = await read_fields_from_record("relations", "*", "reports_to", [emp_id])
            if data:
                data = parse_relations(data)
                data = await populate_relations(data)
                for item in data:
                    del item["reports_to"]
                    del item["emp_id"]
                return data
            else:
                return [] 

    def info(self):
        return """
                This is the worker class and it has the following properties :
                - Reports to
                - Reported to by
                - Department
                Following are the methods provided by this class :
                - See own team hierarchy

        """
