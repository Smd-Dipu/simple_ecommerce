from faker import Faker
from app import app, db
from models import Product
import random

fake = Faker()

def populate_products(n=10000):
    print(f"Generating {n} products...")
    
    # Batch insert for performance
    batch_size = 1000
    products = []
    
    for i in range(n):
        product = Product(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10.0, 1000.0), 2),
            image_url=f"https://picsum.photos/seed/{i}/400/300", # Random image
            stock_quantity=random.randint(0, 100)
        )
        products.append(product)
        
        if len(products) >= batch_size:
            db.session.add_all(products)
            db.session.commit()
            products = []
            print(f"Inserted {i+1} products...")
            
    if products:
        db.session.add_all(products)
        db.session.commit()
        
    print("Done!")

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we already have products
        if Product.query.count() < 10000:
            populate_products()
        else:
            print("Database already populated.")
