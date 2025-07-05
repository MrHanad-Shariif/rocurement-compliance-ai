from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from difflib import SequenceMatcher
import spacy
from fpdf import FPDF
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
nlp = spacy.load("en_core_web_sm")

LEGAL_ENTITIES = [1001, 1002, 1003]
APPROVED_ITEMS = [
    "Office chair",
    "Laptop 15 inch",
    "Printer A4",
    "Desk lamp",
    "Whiteboard large"
]

# AI agent logic
def validate_legal_entity(legal_entity_id):
    if legal_entity_id in LEGAL_ENTITIES:
        return True, "✅ PR linked to correct legal entity"
    else:
        return False, "❌ PR linked to incorrect legal entity"

def validate_quantity_item(item_type, quantity):
    if item_type == 'Laptop' and quantity > 50:
        return False, f"❌ Quantity too high for {item_type}: {quantity}"
    if item_type == 'Chair' and quantity > 500:
        return False, f"❌ Quantity too high for {item_type}: {quantity}"
    return True, "✅ Quantity-item checks passed"

def is_similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def validate_description(description):
    best_match = max(APPROVED_ITEMS, key=lambda x: is_similar(description, x))
    similarity = is_similar(description, best_match)
    if similarity < 0.7:
        return False, f"❌ Description unclear for '{description}'. Closest match: '{best_match}'"
    doc = nlp(description)
    if not list(doc.ents):
        return False, f"❌ NLP check: No entities found in description '{description}'"
    return True, "✅ Item description acceptable"

# Routes
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "result": None})

@app.post("/validate", response_class=HTMLResponse)
async def form_post(
    request: Request,
    legal_entity_id: int = Form(...),
    item_type: List[str] = Form(...),
    description: List[str] = Form(...),
    quantity: List[int] = Form(...)
):
    results = []

    valid, msg = validate_legal_entity(legal_entity_id)
    results.append(msg)
    if not valid:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "result": results,
            "passed": False
        })

    for i in range(len(item_type)):
        valid, msg = validate_quantity_item(item_type[i], quantity[i])
        results.append(msg)
        if not valid:
            return templates.TemplateResponse("form.html", {
                "request": request,
                "result": results,
                "passed": False
            })

        valid, msg = validate_description(description[i])
        results.append(msg)
        if not valid:
            return templates.TemplateResponse("form.html", {
                "request": request,
                "result": results,
                "passed": False
            })

    # If all passed
    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": results,
        "passed": True,
        "legal_entity_id": legal_entity_id,
        "item_types": item_type,
        "descriptions": description,
        "quantities": quantity
    })

@app.post("/generate_rfq", response_class=HTMLResponse)
async def generate_rfq(
    request: Request,
    legal_entity_id: int = Form(...),
    item_type: List[str] = Form(...),
    description: List[str] = Form(...),
    quantity: List[int] = Form(...)
):
    pdf_path = generate_rfq_pdf(legal_entity_id, item_type, description, quantity)
    msg = f"✅ RFQ generated: <a href='/static/{pdf_path}' target='_blank'>Download RFQ PDF</a>"
    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": [msg],
        "passed": False
    })

def generate_rfq_pdf(legal_entity_id, item_types, descriptions, quantities):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Request for Quotation (RFQ)", ln=True, align='C')
    pdf.ln(10)

    # Legal Entity
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Legal Entity ID: {legal_entity_id}", ln=True)
    pdf.ln(5)

    # Table header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Item Type", 1)
    pdf.cell(80, 10, "Description", 1)
    pdf.cell(30, 10, "Quantity", 1)
    pdf.ln()

    # Table content
    pdf.set_font("Arial", '', 12)
    for i in range(len(item_types)):
        pdf.cell(50, 10, item_types[i], 1)
        pdf.cell(80, 10, descriptions[i], 1)
        pdf.cell(30, 10, str(quantities[i]), 1)
        pdf.ln()

    filename = f"rfq_{legal_entity_id}.pdf"
    filepath = os.path.join("static", filename)
    pdf.output(filepath)
    return filename
