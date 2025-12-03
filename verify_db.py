from app import app, db
from models import User, Product, Order
from sqlalchemy import inspect

def verify():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables found: {tables}")
        
        if 'users' in tables:
            try:
                print(f"Users count: {User.query.count()}")
                admin = User.query.filter_by(username='admin').first()
                if admin:
                    print(f"Admin user found: {admin.username}")
                else:
                    print("Admin user NOT found.")
            except Exception as e:
                print(f"Error querying users: {e}")
        
        if 'products' in tables:
            try:
                print(f"Products count: {Product.query.count()}")
            except Exception as e:
                print(f"Error querying products: {e}")

if __name__ == "__main__":
    verify()
