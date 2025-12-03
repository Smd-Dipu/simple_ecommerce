from app import app, db
from models import User

def fix_admin_password():
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user:
            user.password_hash = 'admin123'
            db.session.commit()
            print("Password updated to 'admin123'")
        else:
            print("User not found")

if __name__ == "__main__":
    fix_admin_password()
