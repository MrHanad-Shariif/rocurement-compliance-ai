from sqlalchemy.orm import Session
from app.models.legal_entity import LegalEntity

def get_legal_entities(db: Session):
    return db.query(LegalEntity).all()

def get_legal_entity(db: Session, entity_id: int):
    return db.query(LegalEntity).filter(LegalEntity.id == entity_id).first()

def create_legal_entity(db: Session, name: str, code: str):
    entity = LegalEntity(name=name, code=code)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

def delete_legal_entity(db: Session, entity_id: int):
    entity = db.query(LegalEntity).filter(LegalEntity.id == entity_id).first()
    if entity:
        db.delete(entity)
        db.commit()
    return entity 