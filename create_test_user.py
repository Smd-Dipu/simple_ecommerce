from app import app, db
from models import User

def create_test_user():
    with app.app_context():
        user = User.query.filter_by(username='test_staff').first()
        if not user:
            user = User(username='test_staff', email='staff@example.com', password_hash='password', role='customer')
            db.session.add(user)
            db.session.commit()
            print("Created test_staff user.")
        else:
            print("test_staff user already exists.")

if __name__ == "__main__":
    create_test_user()
