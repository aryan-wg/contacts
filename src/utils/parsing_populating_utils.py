from datetime import datetime
from .db_utils import read_fields_from_record


def parse_requests(requests):
    requests_parsed = []
    for request in requests:
        temp = {
            "request_id": request[0],
            "created_by": request[1],
            "updated_info": request[2],
            "assigned_hr": request[3],
            "remark": request[4],
            "created_at": request[5],
            "update_committed_at": request[6],
            "request_status": request[7],
        }
        requests_parsed.append(temp)

    return requests_parsed


def populate_requests(requests):
    populated = []
    for request in requests:
        time_stamp = datetime.fromtimestamp(request["created_at"])
        request["created_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        if not request["update_committed_at"] == 0:
            time_stamp = datetime.fromtimestamp(request["update_committed_at"])
            request["update_committed_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        record = read_fields_from_record(
            "employees",
            "name",
            "empId",
            [request["created_by"], request["assigned_hr"]],
        )
        request["created_by"] = record[0][0]
        request["assigned_hr"] = record[1][0]
        # print(request)
        populated.append(request)
    return populated


def parse_relations(relations):
    relations_parsed = []
    for relation in relations:
        temp = {
            "reports_to": relation[0],
            "empId": relation[1],
        }
        relations_parsed.append(temp)

    return relations_parsed


def populate_relations(relations):
    populated = []
    for relation in relations:
        if relation["reports_to"] == 0:
            reports_to = {
                "name": None,
                "empId": None,
                "email": None,
                "phone": None,
            }
            relation["reports_to"] = reports_to

        else:
            reports_to_info = read_fields_from_record(
                "employees", "name, email, phone", "empId", [relation["reports_to"]]
            )
            if reports_to_info:
                reports_to = {
                    "name": reports_to_info[0][0],
                    "empId": relation["reports_to"],
                    "email": reports_to_info[0][1],
                    "phone": reports_to_info[0][2],
                }
                relation["reports_to"] = reports_to

        emp_info = read_fields_from_record(
            "employees", "name, email, phone", "empId", [relation["empId"]]
        )
        employee = {
            "name": emp_info[0][0],
            "empId": relation["empId"],
            "email": emp_info[0][1],
            "phone": emp_info[0][2],
        }
        relation["employee"] = employee
        populated.append(relation)
    return populated
