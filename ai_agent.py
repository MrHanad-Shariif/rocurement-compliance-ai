from difflib import SequenceMatcher
import spacy

LEGAL_ENTITIES = [1001, 1002, 1003]
APPROVED_ITEMS = [
    "Office chair",
    "Laptop 15 inch",
    "Printer A4",
    "Desk lamp",
    "Whiteboard large"
]

nlp = spacy.load("en_core_web_sm")

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
