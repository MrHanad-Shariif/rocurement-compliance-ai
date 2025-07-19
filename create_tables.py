from app.db import Base, engine
from app.models import user, rbac, legal_entity, approved_item, validation, item_to_pr

# Import all models so Base.metadata.create_all sees them
def main():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    main() 