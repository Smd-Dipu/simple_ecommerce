from app import app, db
from models import User

def check_admin():
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user:
            print(f"User: {user.username}")
            print(f"Email: {user.email}")
            print(f"Password Hash: {user.password_hash}")
            print(f"Is Admin: {user.is_admin}")
            print(f"Role: {user.role}")
        else:
            print("Admin user not found!")

if __name__ == "__main__":
    check_admin()
