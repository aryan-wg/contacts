from ..employee.employee import Employee
from ...types.general_types import LOG_LEVEL_ENUM
from ...utils.async_pg_db_utils import (
    read_fields_from_record,
    update_one_record,
    write_to_table,
    check_if_exists_in_db,
    delete_from_table,
    read_by_multiple_attributes,
)
from ...utils.general_utils import hash_pass
from ...utils.parsing_populating_utils import parse_requests, populate_requests

from math import ceil
import time

import json


class Admin(Employee):
    def __init__(self, emp_id,logger):
        super().__init__(emp_id,logger)

    async def get_req(self, status_list):
        data = await read_fields_from_record(
            "requests", "*", "request_status", status_list
        )
        if data:
            data = parse_requests(data)
            data = await populate_requests(data)
        return data

    async def get_pending_req(self):
        # for a request to be pending it should have req_status == approved_by_hr
        data = await read_fields_from_record(
            "requests", "*", "request_status", ["approved_by_hr"]
        )
        if data:
            data = parse_requests(data)
            data = await populate_requests(data)
        return data

    async def get_closed_req(self):
        # for a request to be closed it should have req_status == committed or rejected
        self.logger.log(f"admin get reported by", LOG_LEVEL_ENUM.INFO)
        requests = await read_fields_from_record(
            "requests", "*", "request_status", ["committed", "rejected"]
        )
        if requests:
            requests = parse_requests(requests)
            requests = await populate_requests(requests)
        return data

    async def commit_request(self, req_id):
        # get request information
        request = await read_fields_from_record("requests", "*", "request_id", [req_id])
        if not len(request) == 1:
            self.logger.log(f"Request does not exist {req_id}",LOG_LEVEL_ENUM.ERROR)
            raise ValueError("Request does not exist")
        else:
            request = parse_requests(request)
            request = request[0]
            if request["status"] == "approved_by_hr":
                # parse the json obj of update to updated dict
                updated_info = json.loads(request["updated_info"])

                # the address field has sub fields and should be stored as a stringified json obj
                updated_info["address"] = json.dumps(updated_info["address"])

                # update the employee record
                await update_one_record(
                    "employees", updated_info, "empId", request["created_by"]
                )

                # update the request status to committed and add commit time
                request["update_committed_at"] = ceil(time.time())
                request["request_status"] = "committed"
                await update_one_record("requests", request, "request_id", req_id)
                self.logger.log(f"Request commited {req_id}",LOG_LEVEL_ENUM.INFO)
                return True
            else:
                self.logger.log(f"Request can't be commited {req_id} status = {request["status"]}",LOG_LEVEL_ENUM.ERROR)
                raise ValueError("Request can't be committed")

    async def create_new_employee(self, new_employee):
        try:
            if new_employee["reports_to"]!=0 and not await check_if_exists_in_db("employees","empId",new_employee["reports_to"]):
                self.logger.log(f"Reporting to user does not exist {new_employee["reports_to"]}",LOG_LEVEL_ENUM.ERROR)
                raise ValueError("Reporting to user does not exist")
            if await check_if_exists_in_db("employees", "email", new_employee["email"]):
                self.logger.log(f"User with email {new_employee['email']} already exists",LOG_LEVEL_ENUM.ERROR)
                raise ValueError(
                    f"User with email {new_employee['email']} already exists"
                )
            else:
                new_employee["password"] = hash_pass(new_employee["password"])
                created_employee = await write_to_table("employees", new_employee)
                self.logger.log(f"new user created empId = {created_employee["empid"]}",LOG_LEVEL_ENUM.INFO)
                return created_employee
        except ValueError as err:
            raise ValueError(err)
        except Exception as err:
            self.logger.log(f"{str(err)}", LOG_LEVEL_ENUM.ERROR)
            raise Exception(err)

    async def create_new_relation(self, emp_id, reports_to_emp_id):
        try:
            if reports_to_emp_id == 0 or await check_if_exists_in_db(
                    "employees", "empId", reports_to_emp_id
            ):
                new_relation = {}
                new_relation["employee"] = emp_id
                new_relation["reports_to"] = reports_to_emp_id
                created_relation = await write_to_table("relations", new_relation)
                self.logger.log(f"New relation created ",LOG_LEVEL_ENUM.INFO)
                return created_relation
            else:
                self.logger.log(f"employee does not exist in db emp id = {emp_id}",LOG_LEVEL_ENUM.ERROR)
                return False
        except Exception as err:
            self.logger.log(f"{str(err)}", LOG_LEVEL_ENUM.ERROR)
            raise Exception(err)

    async def remove_employee(self, emp_id):
        try:
            if not await check_if_exists_in_db("employees", "empId", emp_id):
                self.logger.log(f"Employee does not exist ",LOG_LEVEL_ENUM.ERROR)
                return False
            else:
                if (
                        len(
                            await read_by_multiple_attributes(
                                "employees", "*", ["user_type", "empId"], ["admin", emp_id]
                            )
                        )
                        == 1
                ):
                    self.logger.log(f"Deleting last admin not allowed ", LOG_LEVEL_ENUM.ERROR)
                    raise ValueError("Deleting last admin not allowed")
                reporting_employees = await read_fields_from_record(
                    "relations", "employee", "reports_to", [emp_id]
                )
                reporting_to = await read_fields_from_record(
                    "relations", "reports_to", "employee", [emp_id]
                )
                reporting_to = reporting_to[0][0]
                reporting_employees = list(
                    map(
                        lambda reporting_employee: reporting_employee[0],
                        reporting_employees,
                    )
                )
                for reporting_employee in reporting_employees:
                    await self.create_new_relation(reporting_employee,reporting_to)
                    # await write_to_table(
                    #     "relations",
                    #     {"employee": reporting_employee, "reports_to": reporting_to},
                    # )
                await delete_from_table("relations", "reports_to", emp_id)
                self.logger.log("Deleted relation")
                await self.delete_employee(emp_id)
                return True
        except ValueError as err:
            raise err
        except Exception as err:
            self.logger.log(f"{str(err)}",LOG_LEVEL_ENUM.ERROR)
            raise err

    async def delete_employee(self, emp_id):
        if not await check_if_exists_in_db("employees", "empId", emp_id):
            self.logger.log("Employee does not exist",LOG_LEVEL_ENUM.ERROR)
            raise ValueError("Employee does not exist.")
        else:
            self.logger.log(f"Deleting employee {emp_id}",LOG_LEVEL_ENUM.INFO)
            return await delete_from_table("employees", "empId", emp_id)

    async def get_reports_to(self, emp_id):
        if not await check_if_exists_in_db("employees", "empId", emp_id):
            self.logger.log(f"Employee does not exist",LOG_LEVEL_ENUM.ERROR)
            raise ValueError("Employee does not exist.")
        else:
            data = await read_fields_from_record(
                "relations", "reports_to", "employee", [emp_id]
            )
            self.logger.log(f"get_reports_to", LOG_LEVEL_ENUM.INFO)
            if data[0][0]:
                return {"emp_id": data[0][0]}
            else:
                return []

    async def update_reports_to(self, emp_id, reports_to_emp_id):
        try:
            if await check_if_exists_in_db("employees", "empid", emp_id):
                if reports_to_emp_id and await check_if_exists_in_db(
                        "employees", "empId", reports_to_emp_id
                ):
                    self.logger.log(f"update_reports_to", LOG_LEVEL_ENUM.INFO)
                    return await update_one_record(
                        "relations",
                        {"reports_to": reports_to_emp_id},
                        "employee",
                        emp_id,
                    )
                elif not reports_to_emp_id:
                    # will run in case when reports to user id is 0 (ie employee does not report to anyone as 0 employee id does not exist in db)
                    self.logger.log(f"update_reports_to", LOG_LEVEL_ENUM.INFO)
                    return await update_one_record(
                        "relations",
                        {"reports_to": reports_to_emp_id},
                        "employee",
                        emp_id,
                    )
                else:
                    raise ValueError("Reporting to employee does not exist")
            else:
                raise ValueError(
                    {"status_code": 404, "detail": "Employee does not exist"}
                )
        except ValueError as err:
            self.logger.log(f"{str(err)}", LOG_LEVEL_ENUM.ERROR)
            raise ValueError(err)
        except Exception as err:
            self.logger.log(f"{str(err)}", LOG_LEVEL_ENUM.ERROR)
            raise err

    async def get_reported_by(self, emp_id):
        if not await check_if_exists_in_db("employees", "empId", emp_id):
            self.logger.log(f"Employee does not exist", LOG_LEVEL_ENUM.ERROR)
            raise ValueError("Employee does not exist.")
        else:
            relations = await read_fields_from_record(
                "relations", "employee", "reports_to", [emp_id]
            )
            relations = [relation[0] for relation in relations]
            self.logger.log(f"admin get reported by", LOG_LEVEL_ENUM.INFO)
            return relations

    def info(self):
        doc = """
            This is the admin user class it has the following methods
            - Edit workers info
            - Add new worker
            - Remove worker
            - Approve a request
        """
        print(doc)
