from src.database.db_setup import create_tables, insert_sample_data
from src.ui.admin_ui import AdminUi
from src.ui.worker_ui import WorkerUi
from src.ui.hr_ui import HrUi
from src.ui.auth_ui import Auth_ui
from src.utils.parsing_populating_utils import populate_relations

from pprint import pprint


def main():
    create_tables()
    # insert_sample_data()


    active_auth_ui = Auth_ui()
    user_obj = active_auth_ui.login()
    active_user_ui = None
    if user_obj.user_type == "admin":
        active_user_ui = AdminUi(user_obj)
    elif user_obj.user_type == "worker":
        active_user_ui = WorkerUi(user_obj)
    elif user_obj.user_type == "hr":
        active_user_ui = HrUi(user_obj)

    if active_user_ui:
        active_user_ui.show_menu()


if __name__ == "__main__":
    main()
