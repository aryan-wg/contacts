from ..employee.employee import Employee
from ...utils.pg_db_utils import read_fields_from_record
from ...utils.parsing_populating_utils import parse_relations, populate_relations

from pprint import pprint


class Worker(Employee):
    # def __init__(self, employee_info):
    #     if len(employee_info) == 5:
    #         super().__init__((*employee_info, "worker"))
    #     elif len(employee_info) == 6:
    #         super().__init__(employee_info)

    def __init__(self):
        super().__init__()

    def reports_to(self, empId):
        data = read_fields_from_record("relations", "*", "employee", [empId])
        if data:
            data = parse_relations(data)
            data = populate_relations(data)
            return data[0]
        else:
            return None

    def reported_by(self, empId):
        data = read_fields_from_record("relations", "*", "reports_to", [empId])
        if data:
            data = parse_relations(data)
            data = populate_relations(data)
            return data
        else:
            return None

    def info(self):
        return """
                This is the worker class and it has the following properties :
                - Reports to
                - Reported to by
                - Department
                Following are the methods provided by this class :
                - See own team hierarchy

        """
