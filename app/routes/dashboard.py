from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db import get_db
from app.auth import check_login
from sqlalchemy.orm import Session
from app.models.validation import Validation
from sqlalchemy import func

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    username = request.cookies.get("user")
    total_prs = db.query(Validation).count()
    pending_prs = db.query(Validation).filter(Validation.result == 'Pending').count()
    approved_prs = db.query(Validation).filter(Validation.result == 'Passed').count()
    # Get item_type counts
    item_type_counts = {}
    for row in db.query(Validation.item_type, func.count(Validation.id)).group_by(Validation.item_type).all():
        item_type, count = row
        item_type_counts[item_type] = count
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard",
        "total_prs": total_prs,
        "pending_prs": pending_prs,
        "approved_prs": approved_prs,
        "username": username,
        "item_type_counts": item_type_counts
    }) 