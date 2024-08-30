from .db_utils import read_fields_from_record
from datetime import datetime, time

def parse_requests(requests):
    print(requests)
    requests_parsed = []
    for request in requests:
        temp = {
            "request_id": request[0],
            "created_by": request[1],
            "updated_info": request[2],
            "assigned_hr": request[3],
            "remark": request[4],
            "created_at": request[5],
            "update_commited_at": request[6],
            "request_status": request[7],
        }
        requests_parsed.append(temp)

    return requests_parsed


def populate_requests(requests):
    populated = []
    for request in requests:
        time_stamp = datetime.fromtimestamp(request['created_at'])
        request["created_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        if not request["update_commited_at"] == 0:
            time_stamp = datetime.fromtimestamp(request['update_commited_at'])
            request["update_commited_at"] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        record = read_fields_from_record(
            "employees",
            "name",
            "empId",
            [request["created_by"], request["assigned_hr"]],
        )
        request["created_by"] = record[0][0]
        request["assigned_hr"] = record[1][0]
        print(request)
        populated.append(request)
    return populated 


def parse_relations(relations):
    relations_parsed = []
    for relation in relations:
        temp = {
            "reports_to": relation[0],
            "employee": relation[1],
            "team": relation[2],
        }
        relations_parsed.append(temp)

    return relations_parsed
