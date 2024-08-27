from ..employee.employee import Employee


class Worker(Employee):
    def __init__(self, *args):
        reports_to, reported_by, personal_info = args

        self.reports_to = reports_to
        self.reported_by = reported_by
        super().__init__(*personal_info)
        print("new worker instantiated", self.name)

    def see_own_team(self):
        print("seeing own team")

    def save(self):
        print("saving the worker info to the db")

    def info(self):
        return """
                This is the worker class and it has the following properties :
                - Reports to
                - Reported to by
                - Department
                Following are the methods provided by this class :
                - See own team hierarchy

        """
