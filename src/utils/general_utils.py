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
