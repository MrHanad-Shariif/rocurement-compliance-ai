from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.legal_entity import LegalEntity
from app.models.approved_item import ApprovedItem
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# --- Legal Entities ---
@router.get("/legal_entities", response_class=HTMLResponse)
def legal_entities(request: Request, db: Session = Depends(get_db)):
    entities = db.query(LegalEntity).all()
    return templates.TemplateResponse("legel_entity.html", {"request": request, "legal_entities": entities})

@router.post("/add_legal_entity", response_class=HTMLResponse)
def add_legal_entity(request: Request, name: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    entity = LegalEntity(name=name, code=code)
    db.add(entity)
    db.commit()
    return RedirectResponse(url="/legal_entities", status_code=303)

@router.post("/edit_legal_entity/{entity_id}", response_class=HTMLResponse)
def edit_legal_entity(request: Request, entity_id: int, name: str = Form(...), code: str = Form(...), db: Session = Depends(get_db)):
    entity = db.query(LegalEntity).filter(LegalEntity.id == entity_id).first()
    if entity:
        entity.name = name
        entity.code = code
        db.commit()
    return RedirectResponse(url="/legal_entities", status_code=303)

@router.post("/delete_legal_entity/{entity_id}", response_class=HTMLResponse)
def delete_legal_entity(request: Request, entity_id: int, db: Session = Depends(get_db)):
    entity = db.query(LegalEntity).filter(LegalEntity.id == entity_id).first()
    if entity:
        db.delete(entity)
        db.commit()
    return RedirectResponse(url="/legal_entities", status_code=303)

# --- Approved Items ---
@router.get("/approved_items", response_class=HTMLResponse)
def approved_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(ApprovedItem).all()
    return templates.TemplateResponse("approved_items.html", {"request": request, "approved_items": items})

@router.post("/add_approved_item", response_class=HTMLResponse)
def add_approved_item(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    item = ApprovedItem(name=name)
    db.add(item)
    db.commit()
    return RedirectResponse(url="/approved_items", status_code=303)

@router.post("/edit_approved_item/{item_id}", response_class=HTMLResponse)
def edit_approved_item(request: Request, item_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    item = db.query(ApprovedItem).filter(ApprovedItem.id == item_id).first()
    if item:
        item.name = name
        db.commit()
    return RedirectResponse(url="/approved_items", status_code=303)

@router.post("/delete_approved_item/{item_id}", response_class=HTMLResponse)
def delete_approved_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(ApprovedItem).filter(ApprovedItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return RedirectResponse(url="/approved_items", status_code=303) 