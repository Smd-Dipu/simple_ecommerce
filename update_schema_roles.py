from app import app, db
from models import User
import os

def update_db_roles():
    with app.app_context():
        try:
            # Try to query role. If it fails, we need to add it.
            User.query.filter_by(role='admin').first()
            print("Schema looks correct (role column exists).")
        except Exception:
            print("Adding role column...")
            # SQLite specific
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'customer'"))
                conn.commit()
            print("Column added.")

        # Update existing admin to have 'admin' role
        admin = User.query.filter_by(username='admin').first()
        if admin:
            admin.role = 'admin'
            db.session.commit()
            print("Updated admin user role to 'admin'.")

if __name__ == "__main__":
    update_db_roles()
