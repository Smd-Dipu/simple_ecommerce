from faker import Faker
from app import app, db
from models import User, Product, Order, OrderItem
import random
from datetime import datetime, timedelta

fake = Faker()

def populate_orders(n=100):
    print(f"Generating {n} orders...")
    
    users = User.query.all()
    if not users:
        # Create a default user
        user = User(username='guest', email='guest@example.com')
        db.session.add(user)
        db.session.commit()
        users = [user]
        
    products = Product.query.limit(100).all() # Just use first 100 products
    
    for i in range(n):
        user = random.choice(users)
        # Random date in last 30 days
        created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        
        order = Order(
            user_id=user.id,
            total_price=0,
            status=random.choice(['Pending', 'Completed', 'Shipped', 'Cancelled']),
            created_at=created_at
        )
        db.session.add(order)
        db.session.commit() # Commit to get ID
        
        # Add items
        total_price = 0
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            price = product.price
            
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=price
            )
            db.session.add(item)
            total_price += price * quantity
            
        order.total_price = total_price
        db.session.add(order)
        
        if i % 10 == 0:
            db.session.commit()
            print(f"Created {i} orders...")
            
    db.session.commit()
    print("Done!")

if __name__ == "__main__":
    with app.app_context():
        populate_orders()
