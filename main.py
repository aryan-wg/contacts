from src.routers.admin_routes import admin_router 
from src.routers.auth_routes import auth_router
from fastapi.middleware.cors import CORSMiddleware
# from src.database.db_setup import create_tables, insert_sample_data
# from src.ui.admin_ui import AdminUi
# from src.ui.worker_ui import WorkerUi
# from src.ui.hr_ui import HrUi
# from src.ui.auth_ui import Auth_ui
# from src.utils.parsing_populating_utils import populate_relations
#
# from pprint import pprint
#
from fastapi import FastAPI
import yaml

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    with open("openapi.yaml", "r") as f:
        return yaml.safe_load(f)

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router,tags=["auth"], prefix="/v1/auth")

@app.get("/test")
def test():
    return {"Status":"API running"}

app.include_router(admin_router,prefix = "/admin")


# def main():
#     create_tables()
#     # insert_sample_data()
#     active_auth_ui = Auth_ui()
#     user_obj = active_auth_ui.login()
#     active_user_ui = None
#     if user_obj.user_type == "admin":
#         # here the user_obj is a good example of dependency inverison  
#         active_user_ui = AdminUi(user_obj)
#     elif user_obj.user_type == "worker":
#         active_user_ui = WorkerUi(user_obj)
#     elif user_obj.user_type == "hr":
#         active_user_ui = HrUi(user_obj)
#
#     if active_user_ui:
#         active_user_ui.show_menu()
#
#
# if __name__ == "__main__":
#     main()
