from fastapi import APIRouter, Request, Form, Path, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
from app.db import get_db
from app.auth import check_login
from app.ai_agent import validate_legal_entity, validate_quantity_item, validate_description
from app.pdf_utils import generate_rfq_pdf, generate_multilingual_rfq_pdf, generate_rfp_pdf
from app.email_utils import email_notifier
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Remove the /pr_form route and any references to pr_form.html

@router.post("/validate", response_class=HTMLResponse)
async def validate_pr(request: Request):
    form = await request.form()
    legal_entity_id = int(form["legal_entity_id"])
    vendor_ids = form.getlist("vendor_ids")
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
        # Redirect back to PR table with error message
        response = RedirectResponse(url="/pr_table?error=" + msg.replace(" ", "%20"), status_code=302)
        return response

    for i in range(len(item_type)):
        valid, msg = validate_quantity_item(item_type[i], quantity[i])
        results.append(msg)
        if not valid:
            # Redirect back to PR table with error message
            response = RedirectResponse(url="/pr_table?error=" + msg.replace(" ", "%20"), status_code=302)
            return response
        valid, msg = validate_description(description[i])
        results.append(msg)
        if not valid:
            # Redirect back to PR table with error message
            response = RedirectResponse(url="/pr_table?error=" + msg.replace(" ", "%20"), status_code=302)
            return response

    conn = get_db()
    cur = conn.cursor()
    for i in range(len(item_type)):
        cur.execute(
            "INSERT INTO validations (legal_entity_id, item_type, description, quantity, result, vendor_ids) VALUES (%s, %s, %s, %s, %s, %s)",
            (legal_entity_id, item_type[i], description[i], quantity[i], "Passed", ','.join(vendor_ids))
        )
    conn.commit()
    cur.close()
    conn.close()

    # Redirect back to PR table with success message
    success_msg = f"PR for Legal Entity {legal_entity_id} created successfully!"
    response = RedirectResponse(url="/pr_table?success=" + success_msg.replace(" ", "%20"), status_code=302)
    return response

@router.get("/pr_table", response_class=HTMLResponse)
async def pr_table(request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM validations")
    prs = cur.fetchall()
    cur.execute("SELECT id, name, email, language FROM vendors")
    vendors = cur.fetchall()
    cur.close()
    conn.close()

    # Check if email is configured
    import os
    email_configured = all([
        os.getenv("SMTP_SERVER"),
        os.getenv("SMTP_PORT"),
        os.getenv("SMTP_USERNAME"),
        os.getenv("SMTP_PASSWORD"),
        os.getenv("FROM_EMAIL"),
        os.getenv("FROM_NAME")
    ])

    # Parse rfq_file JSON if possible
    def parse_rfq_file(rfq_file):
        import json
        try:
            return json.loads(rfq_file) if rfq_file and rfq_file.strip().startswith('{') else rfq_file
        except Exception:
            return rfq_file
    prs = [
        list(pr[:7]) + [parse_rfq_file(pr[7])] + list(pr[8:])
        if len(pr) > 7 else pr
        for pr in prs
    ]

    return templates.TemplateResponse("pr_table.html", {
        "request": request,
        "title": "PR Table",
        "prs": prs,
        "vendors": vendors,
        "email_configured": email_configured
    })

@router.get("/edit_pr/{pr_id}", response_class=HTMLResponse)
async def edit_pr_get(request: Request, pr_id: int = Path(...)):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, legal_entity_id, item_type, description, quantity FROM validations WHERE id=%s", (pr_id,))
    pr = cur.fetchone()
    cur.close()
    conn.close()
    if not pr:
        return HTMLResponse("PR not found", status_code=404)
    return templates.TemplateResponse("edit_pr.html", {"request": request, "pr": pr})

@router.post("/edit_pr/{pr_id}", response_class=HTMLResponse)
async def edit_pr_post(request: Request, pr_id: int = Path(...), legal_entity_id: int = Form(...), item_type: str = Form(...), description: str = Form(...), quantity: int = Form(...)):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE validations SET legal_entity_id=%s, item_type=%s, description=%s, quantity=%s WHERE id=%s", (legal_entity_id, item_type, description, quantity, pr_id))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/pr_table", status_code=302)

@router.post("/delete_pr/{pr_id}", response_class=HTMLResponse)
async def delete_pr(request: Request, pr_id: int = Path(...)):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM validations WHERE id=%s", (pr_id,))
    conn.commit()
    cur.close()
    conn.close()
    return RedirectResponse(url="/pr_table", status_code=302)

@router.post("/generate_rfq", response_class=HTMLResponse)
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
    cur = conn.cursor()
    cur.execute("UPDATE validations SET rfq_file=%s WHERE legal_entity_id=%s", (pdf_path, legal_entity_id))
    conn.commit()
    cur.close()
    conn.close()
    msg = f"✅ RFQ generated: <a href='/download/{pdf_path}' target='_blank'>Download RFQ PDF</a>"
    # Redirect back to PR table with success message
    success_msg = f"RFQ for Legal Entity {legal_entity_id} generated successfully!"
    response = RedirectResponse(url="/pr_table?success=" + success_msg.replace(" ", "%20"), status_code=302)
    return response

@router.post("/generate_and_notify", response_class=HTMLResponse)
async def generate_and_notify(request: Request):
    """Generate multilingual RFQ/RFP and send notifications to vendors"""
    form = await request.form()
    legal_entity_id = int(form["legal_entity_id"])
    item_type = form.getlist("item_type")
    description = form.getlist("description")
    quantity_strs = form.getlist("quantity")
    quantity = [int(q) for q in quantity_strs]
    vendor_ids = form.getlist("vendor_ids")
    document_type = form.get("document_type", "rfq")  # rfq or rfp
    language = form.get("language", "en")
    # Ensure data directory exists
    os.makedirs("data/private_pdfs", exist_ok=True)
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    # Get vendor information
    conn = get_db()
    cur = conn.cursor()
    vendor_ids_int = [int(vid) for vid in vendor_ids]
    cur.execute("SELECT id, name, email, language FROM vendors WHERE id = ANY(%s)", (vendor_ids_int,))
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    pdf_files = {}
    notification_results = {}
    for vendor in vendors:
        vendor_id, vendor_name, vendor_email, vendor_language = vendor
        # Use selected language from form
        pdf_lang = language
        if document_type == "rfp":
            pdf_filename = generate_rfp_pdf(
                legal_entity_id=legal_entity_id,
                item_types=item_type,
                descriptions=description,
                quantities=quantity,
                vendor_ids=','.join(vendor_ids),
                language=pdf_lang
            )
        else:
            pdf_filename = generate_multilingual_rfq_pdf(
                legal_entity_id=legal_entity_id,
                item_types=item_type,
                descriptions=description,
                quantities=quantity,
                vendor_ids=','.join(vendor_ids),
                language=pdf_lang
            )
        pdf_path = os.path.join("data/private_pdfs", pdf_filename)
        pdf_files[pdf_lang] = pdf_path
        for i in range(len(item_type)):
            success = email_notifier.send_rfq_notification(
                vendor_email=vendor_email,
                vendor_name=vendor_name,
                vendor_language=pdf_lang,
                legal_entity_id=legal_entity_id,
                item_type=item_type[i],
                description=description[i],
                quantity=quantity[i],
                pdf_path=pdf_path
            )
            notification_results[f"{vendor_email}_{i}"] = success
    conn = get_db()
    cur = conn.cursor()
    pdf_files_json = json.dumps(pdf_files)
    cur.execute("UPDATE validations SET rfq_file=%s WHERE legal_entity_id=%s", (pdf_files_json, legal_entity_id))
    conn.commit()
    cur.close()
    conn.close()
    successful_notifications = sum(1 for result in notification_results.values() if result)
    total_notifications = len(notification_results)
    success_msg = f"{document_type.upper()} generated and {successful_notifications}/{total_notifications} notifications sent to vendors!"
    response = RedirectResponse(url="/pr_table?success=" + success_msg.replace(" ", "%20"), status_code=302)
    return response

@router.post("/bulk_notify_vendors", response_class=HTMLResponse)
async def bulk_notify_vendors(request: Request):
    """Send notifications to multiple vendors for existing PR"""
    form = await request.form()
    pr_id = int(form["pr_id"])
    vendor_ids = form.getlist("vendor_ids")
    
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    
    # Get PR information
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT legal_entity_id, item_type, description, quantity FROM validations WHERE id=%s", (pr_id,))
    pr_data = cur.fetchone()
    
    if not pr_data:
        return RedirectResponse(url="/pr_table?error=PR not found", status_code=302)
    
    legal_entity_id, item_type, description, quantity = pr_data
    
    # Get vendor information
    vendor_ids_int = [int(vid) for vid in vendor_ids]
    cur.execute("SELECT id, name, email, language FROM vendors WHERE id = ANY(%s)", (vendor_ids_int,))
    vendors = cur.fetchall()
    cur.close()
    conn.close()
    
    # Send notifications to each vendor
    notification_results = {}
    
    for vendor in vendors:
        vendor_id, vendor_name, vendor_email, vendor_language = vendor
        
        success = email_notifier.send_rfq_notification(
            vendor_email=vendor_email,
            vendor_name=vendor_name,
            vendor_language=vendor_language,
            legal_entity_id=legal_entity_id,
            item_type=item_type,
            description=description,
            quantity=quantity
        )
        notification_results[vendor_email] = success
    
    # Count successful notifications
    successful_notifications = sum(1 for result in notification_results.values() if result)
    total_notifications = len(notification_results)
    
    success_msg = f"Notifications sent to {successful_notifications}/{total_notifications} vendors!"
    response = RedirectResponse(url="/pr_table?success=" + success_msg.replace(" ", "%20"), status_code=302)
    return response

@router.get("/download/{filename}")
async def download(filename: str, request: Request):
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    filepath = os.path.join("data/private_pdfs", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename)
    else:
        return HTMLResponse("File not found", status_code=404)

@router.get("/download_pdfs")
async def download_all_pdfs(request: Request):
    """Download all generated PDFs as a zip file"""
    auth_check = check_login(request)
    if auth_check:
        return auth_check
    
    import zipfile
    import tempfile
    
    pdf_dir = "data/private_pdfs"
    if not os.path.exists(pdf_dir):
        raise HTTPException(status_code=404, detail="No PDFs found")
    
    # Create temporary zip file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w') as zipf:
            for filename in os.listdir(pdf_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_dir, filename)
                    zipf.write(file_path, filename)
    
    return FileResponse(
        tmp_file.name, 
        filename="generated_pdfs.zip",
        media_type="application/zip"
    ) 