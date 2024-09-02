from ..employee.employee import Employee
from ...utils.db_utils import read_fields_from_record
from ...utils.general_utils import parse_relations

from pprint import pprint

class Worker(Employee):
    def __init__(self, employee_info):
        super().__init__(employee_info)
        self.type = "worker"
        self.reports_to = self.get_reports_to()
        self.reported_by = self.get_reported_by()
        # print("new worker instantiated", self.name)

    def get_reports_to(self):
        data = read_fields_from_record("relations","*","employee",[self.empId]) 
        if data:
            data = parse_relations(data)
            # pprint(data)
            return data
        else:
            return None

    def get_reported_by(self):
        data = read_fields_from_record("relations","*","reports_to",[self.empId]) 
        if data:
            data = parse_relations(data)
            # pprint(data)
            return data
        else:
            return None

    def my_team(self):
        i_report_to = read_fields_from_record("relations","reports_to","employee",self.empId)
        head = i_report_to
        team_list = [i_report_to,self.empId]
        while not head == 0:
            higher = read_fields_from_record("relations","reports_to","employee",head)
            print(higher)
            team_list.insert(0,higher[0])
            head = higher[0]
        while not head == None:
            reports_to_me = read_fields_from_record("relations","employee","reports_to",head)
            team_list.append(reports_to_me[0])
            head = reports_to_me[0]
        return team_list

    def info(self):
        return """
                This is the worker class and it has the following properties :
                - Reports to
                - Reported to by
                - Department
                Following are the methods provided by this class :
                - See own team hierarchy

        """
