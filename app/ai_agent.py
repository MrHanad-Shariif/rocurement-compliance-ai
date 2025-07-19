import requests
from difflib import SequenceMatcher
import spacy
import os
from app.models.legal_entity import LegalEntity
from app.models.approved_item import ApprovedItem

nlp = spacy.load("en_core_web_sm")

def get_approved_items(db):
    return [item.name for item in db.query(ApprovedItem).all()]

def validate_legal_entity(db, legal_entity_id):
    entity = db.query(LegalEntity).filter(LegalEntity.id == legal_entity_id).first()
    if entity:
        return True, "✅ PR linked to correct legal entity"
    else:
        return False, "❌ PR linked to incorrect legal entity"

def validate_quantity_item(item_type, quantity):
    # Add more rules as needed
    if item_type == 'Laptop' and quantity > 50:
        return False, f"❌ Quantity too high for {item_type}: {quantity}"
    if item_type == 'Chair' and quantity > 500:
        return False, f"❌ Quantity too high for {item_type}: {quantity}"
    return True, "✅ Quantity-item checks passed"

def is_similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def validate_description(db, description):
    approved_items = get_approved_items(db)
    if not approved_items:
        return False, "❌ No approved items found in the system."
    description_lower = description.lower()
    # 1. Keyword/approved item matching
    for item in approved_items:
        if item.lower() in description_lower:
            # 2. Optional: spaCy NER for extra insight
            doc = nlp(description)
            entities = [ent.label_ for ent in doc.ents]
            if entities:
                return True, f"✅ Description contains approved item '{item}' and entities: {entities}"
            else:
                return True, f"✅ Description contains approved item '{item}', but no named entities detected (still accepted)."
    # 3. Optional: Fuzzy matching fallback
    from difflib import SequenceMatcher
    for item in approved_items:
        if SequenceMatcher(None, description_lower, item.lower()).ratio() > 0.5:
            return True, f"✅ Description is similar to approved item '{item}'."
    return False, "❌ Description does not mention or resemble any approved item."
