from fastapi import APIRouter, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import get_psycopg2_conn
from app.auth import check_login, create_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@router.post("/users", response_class=HTMLResponse)
async def register_user(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    error = None
    success = None
    if not username or not password or not role:
        error = "All fields are required."
    else:
        if create_user(username, password, role):
            success = f"User '{username}' registered successfully."
        else:
            error = "Username already exists."
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "error": error, "success": success})

@router.get("/vendors", response_class=HTMLResponse)
async def vendors_page(request: Request):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, language FROM vendors")
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors, "title": "Vendors"})

@router.post("/add_vendor", response_class=HTMLResponse)
async def add_vendor(request: Request, name: str = Form(...), email: str = Form(...), language: str = Form(...)):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    error = None
    success = None
    if not name or not email or not language:
        error = "All fields are required."
    else:
        try:
            conn = get_psycopg2_conn()
            cur = conn.cursor()
            cur.execute("INSERT INTO vendors (name, email, language) VALUES (%s, %s, %s)", (name, email, language))
            conn.commit()
            success = f"Vendor '{name}' added successfully."
        except Exception as e:
            conn.rollback()
            error = f"Error adding vendor: {str(e)}"
        finally:
            cur.close()
            conn.close()
    # Fetch updated vendor list
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, language FROM vendors")
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors, "title": "Vendors", "error": error, "success": success})

@router.post("/edit_vendor/{vendor_id}", response_class=HTMLResponse)
async def edit_vendor(request: Request, vendor_id: int = Path(...), name: str = Form(...), email: str = Form(...), language: str = Form(...)):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    error = None
    success = None
    try:
        conn = get_psycopg2_conn()
        cur = conn.cursor()
        cur.execute("UPDATE vendors SET name=%s, email=%s, language=%s WHERE id=%s", (name, email, language, vendor_id))
        conn.commit()
        success = f"Vendor '{name}' updated successfully."
    except Exception as e:
        conn.rollback()
        error = f"Error updating vendor: {str(e)}"
    finally:
        cur.close()
        conn.close()
    # Fetch updated vendor list
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, language FROM vendors")
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors, "title": "Vendors", "error": error, "success": success})

@router.post("/delete_vendor/{vendor_id}", response_class=HTMLResponse)
async def delete_vendor(request: Request, vendor_id: int = Path(...)):
    auth_check = check_login(request, required_role="admin")
    if auth_check:
        return auth_check
    error = None
    success = None
    try:
        conn = get_psycopg2_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM vendors WHERE id=%s", (vendor_id,))
        conn.commit()
        success = f"Vendor deleted successfully."
    except Exception as e:
        conn.rollback()
        error = f"Error deleting vendor: {str(e)}"
    finally:
        cur.close()
        conn.close()
    # Fetch updated vendor list
    conn = get_psycopg2_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, language FROM vendors")
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse("vendors.html", {"request": request, "vendors": vendors, "title": "Vendors", "error": error, "success": success}) 