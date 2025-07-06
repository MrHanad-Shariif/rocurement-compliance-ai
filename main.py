from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

import os

from ai_agent import validate_legal_entity, validate_quantity_item, validate_description
from pdf_utils import generate_rfq_pdf
from auth import check_login, verify_user
from db import get_db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login")


# --- AUTH ROUTES ---
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    user = verify_user(username, password)
    if user:
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("user", username)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user")
    return response


# --- DASHBOARD ROUTE ---
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check

    conn = get_db()
    total_prs = conn.execute("SELECT COUNT(*) FROM validations").fetchone()[0]
    pending_prs = conn.execute("SELECT COUNT(*) FROM validations WHERE result = 'Pending'").fetchone()[0]
    approved_prs = conn.execute("SELECT COUNT(*) FROM validations WHERE result = 'Passed'").fetchone()[0]
    conn.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard",
        "total_prs": total_prs,
        "pending_prs": pending_prs,
        "approved_prs": approved_prs
    })


# --- PR pr_form ---
@app.get("/pr_form", response_class=HTMLResponse)
async def Form(request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    return templates.TemplateResponse("pr_form.html", {"request": request, "title": "New PR"})
@app.post("/validate", response_class=HTMLResponse)
async def validate_pr(request: Request):
    form = await request.form()
    legal_entity_id = int(form["legal_entity_id"])
    item_type = form.getlist("item_type")
    description = form.getlist("description")
    quantity_strs = form.getlist("quantity")
    quantity = [int(q) for q in quantity_strs]

    auth_check = check_login(request)
    if auth_check:
        return auth_check

    results = []

    valid, msg = validate_legal_entity(legal_entity_id)
    results.append(msg)
    if not valid:
        return templates.TemplateResponse("pr_form.html", {"request": request, "result": results, "passed": False})

    for i in range(len(item_type)):
        valid, msg = validate_quantity_item(item_type[i], quantity[i])
        results.append(msg)
        if not valid:
            return templates.TemplateResponse("pr_form.html", {"request": request, "result": results, "passed": False})

        valid, msg = validate_description(description[i])
        results.append(msg)
        if not valid:
            return templates.TemplateResponse("pr_form.html", {"request": request, "result": results, "passed": False})

    conn = get_db()
    for i in range(len(item_type)):
        conn.execute(
            "INSERT INTO validations (legal_entity_id, item_type, description, quantity, result) VALUES (?, ?, ?, ?, ?)",
            (legal_entity_id, item_type[i], description[i], quantity[i], "Passed")
        )
    conn.commit()
    conn.close()

    return templates.TemplateResponse("pr_form.html", {
        "request": request,
        "result": results,
        "passed": True,
        "legal_entity_id": legal_entity_id,
        "item_types": item_type,
        "descriptions": description,
        "quantities": quantity
    })




# --- PR TABLE ---
@app.get("/pr_table", response_class=HTMLResponse)
async def pr_table(request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check

    conn = get_db()
    prs = conn.execute("SELECT * FROM validations").fetchall()
    conn.close()

    return templates.TemplateResponse("pr_table.html", {
        "request": request,
        "title": "Purchase Table",
        "prs": prs
    })

@app.post("/generate_rfq", response_class=HTMLResponse)
async def generate_rfq(request: Request):
    form = await request.form()
    legal_entity_id = int(form["legal_entity_id"])
    item_type = form.getlist("item_type")
    description = form.getlist("description")
    quantity_strs = form.getlist("quantity")
    quantity = [int(q) for q in quantity_strs]

    auth_check = check_login(request)
    if auth_check:
        return auth_check

    pdf_path = generate_rfq_pdf(legal_entity_id, item_type, description, quantity)

    conn = get_db()
    conn.execute("UPDATE validations SET rfq_file=? WHERE legal_entity_id=?", (pdf_path, legal_entity_id))
    conn.commit()
    conn.close()

    msg = f"✅ RFQ generated: <a href='/download/{pdf_path}' target='_blank'>Download RFQ PDF</a>"
    return templates.TemplateResponse("pr_form.html", {
        "request": request,
        "result": [msg],
        "passed": False
    })



# --- FILE DOWNLOAD ---
@app.get("/download/{filename}")
async def download(filename: str, request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check

    filepath = os.path.join("private_pdfs", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename)
    else:
        return HTMLResponse("File not found", status_code=404)
