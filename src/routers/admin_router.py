from fastapi import APIRouter

admin_router = APIRouter()

@admin_router.get("/test")
def test_admin():
    return {"Status":"Admin router running"}

@admin_router.get("/pending_requests")
def get_pending_requests(admin):
    pass

@admin_router.patch("/commit_request")
def commit_request(admin,request_id):
    pass

@admin_router.post("/create_emp")
def create_new_employee(admin,employee_info):
    pass

@admin_router.get("/commit_requests")
def get_committed_requests(admin):
    pass


