from app import app, db
from models import Product

def add_categories():
    """Add category column and assign random categories to existing products"""
    with app.app_context():
        try:
            # Try to query category. If it fails, we need to add it.
            Product.query.filter_by(category='Electronics').first()
            print("Category column already exists.")
        except Exception:
            print("Adding category column...")
            # SQLite specific
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE products ADD COLUMN category VARCHAR(100) DEFAULT 'General'"))
                conn.commit()
            print("Column added.")

        # Assign categories to existing products
        categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Toys', 'Beauty', 'Automotive']
        products = Product.query.all()
        
        import random
        for product in products:
            if not product.category or product.category == 'General':
                product.category = random.choice(categories)
        
        db.session.commit()
        print(f"Updated {len(products)} products with categories.")

if __name__ == "__main__":
    add_categories()
