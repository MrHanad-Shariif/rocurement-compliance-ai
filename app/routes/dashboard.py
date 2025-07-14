from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db import get_db
from app.auth import check_login

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    username = request.cookies.get("user")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM validations")
    total_prs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM validations WHERE result = 'Pending'")
    pending_prs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM validations WHERE result = 'Passed'")
    approved_prs = cur.fetchone()[0]
    cur.execute("SELECT item_type, COUNT(*) FROM validations GROUP BY item_type")
    item_type_counts = dict(cur.fetchall())
    cur.close()
    conn.close()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard",
        "total_prs": total_prs,
        "pending_prs": pending_prs,
        "approved_prs": approved_prs,
        "username": username,
        "item_type_counts": item_type_counts
    }) 