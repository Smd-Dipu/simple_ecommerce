from app import app, db
from populate_db import populate_products
from create_admin import create_admin_user

def reset_database():
    print("WARNING: This will delete all data in the database!")
    confirm = input("Are you sure? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        
        print("Populating data...")
        populate_products(n=100) # Smaller number for quick reset, or keep 10000? Let's do 100 for speed, user can run populate_db for more.
        # Actually, let's stick to a reasonable default or call populate_products without args (defaults to 10000)
        # But 10000 takes time. Let's do 1000.
        
    # populate_products is designed to be standalone, but we can import it.
    # Wait, populate_products in populate_db.py has a default n=10000.
    # Let's just call it.
    
    # Re-import to ensure we use the function correctly
    # populate_products() prints its own status.
    
    # We also need to create admin
    create_admin_user()
    
    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()
