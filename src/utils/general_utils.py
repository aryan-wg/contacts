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
