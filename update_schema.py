from app import app, db
from models import User
import os

def update_db():
    with app.app_context():
        # Since SQLite doesn't support ALTER TABLE easily with SQLAlchemy without migration tools,
        # and this is a simple demo, we will check if we need to rebuild or if we can just add the column via raw SQL.
        # But for simplicity and robustness in this demo environment, let's try to add the admin user if table exists,
        # or handle the schema change.
        
        # Simplest approach for this demo: Drop and recreate Users table if it doesn't have is_admin
        # OR just use raw SQL to add the column.
        
        try:
            # Try to query is_admin. If it fails, we need to add it.
            User.query.filter_by(is_admin=True).first()
            print("Schema looks correct.")
        except Exception:
            print("Adding is_admin column...")
            # SQLite specific
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                conn.commit()
            print("Column added.")

        # Create Admin User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            # In real app, hash this!
            admin = User(
                username='admin', 
                email='admin@example.com', 
                password_hash='admin', 
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            # Ensure existing admin has is_admin=True
            if not admin.is_admin:
                admin.is_admin = True
                db.session.commit()
                print("Updated existing admin user privileges.")
            print("Admin user already exists.")

if __name__ == "__main__":
    update_db()
