from app import app, db
from models import User

def create_admin_user():
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            # Note: In a real app, password should be hashed. 
            # But based on admin.py logic: user.password_hash == password (plain text comparison for this simple app?)
            # Let's check models.py to be sure about password hashing. 
            # But admin.py L34 says: user.password_hash == password. So it seems plain text or simple hash.
            # create_test_user.py uses 'password' as password_hash.
            
            admin = User(
                username='admin', 
                email='admin@example.com', 
                password_hash='admin123', 
                role='admin',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Created 'admin' user with password 'admin123'.")
        else:
            print("'admin' user already exists.")
            # Ensure it is admin
            if not admin.is_admin:
                admin.is_admin = True
                admin.role = 'admin'
                db.session.commit()
                print("Updated 'admin' user to have admin privileges.")

if __name__ == "__main__":
    create_admin_user()
