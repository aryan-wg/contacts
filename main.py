from src.database.db_setup import create_tables, insert_sample_data
from src.ui.admin_ui import Admin_interface
from src.ui.worker_ui import Worker_interface
from src.ui.hr_ui import Hr_interface
from src.ui.auth_ui import Auth_interface

def main():
    create_tables()
    # insert_sample_data()

    active_auth_ui = Auth_interface()
    user_obj = active_auth_ui.login()
    active_user_ui = None
    if user_obj.type == "admin":
        active_user_ui = Admin_interface(user_obj)
    elif user_obj.type == "worker":
        active_user_ui = Worker_interface(user_obj)
    elif user_obj.type == "hr":
        active_user_ui = Hr_interface(user_obj)

    active_user_ui.show_menue()

if __name__ == "__main__":
    main()
