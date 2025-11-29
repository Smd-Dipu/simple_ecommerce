from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Product, User, Order, OrderItem

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    per_page = 20
    
    # Get all unique categories for sidebar
    categories = db.session.query(Product.category).distinct().order_by(Product.category).all()
    categories = [c[0] for c in categories if c[0]]
    
    # Filter by category if specified
    if category:
        products = Product.query.filter_by(category=category).paginate(page=page, per_page=per_page, error_out=False)
    else:
        products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('index.html', products=products, categories=categories, selected_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = []
    total_price = 0
    for pid, quantity in cart_items.items():
        product = Product.query.get(int(pid))
        if product:
            total = product.price * quantity
            products.append({'product': product, 'quantity': quantity, 'total': total})
            total_price += total
    return render_template('cart.html', products=products, total_price=total_price)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart_items = session.get('cart', {})
    cart_items[str(product_id)] = cart_items.get(str(product_id), 0) + quantity
    session['cart'] = cart_items
    flash('Item added to cart', 'success')
    return redirect(url_for('index'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Mock checkout logic
        cart_items = session.get('cart', {})
        if not cart_items:
            flash('Your cart is empty', 'warning')
            return redirect(url_for('index'))
        
        # Create a dummy user for this example if not logged in
        # In a real app, we'd require login
        user = User.query.first()
        if not user:
            # Create a default user if none exists
            user = User(username='guest', email='guest@example.com')
            db.session.add(user)
            db.session.commit()

        total_price = 0
        order = Order(user_id=user.id, total_price=0, status='Completed')
        db.session.add(order)
        db.session.commit() # Commit to get ID

        for pid, quantity in cart_items.items():
            product = Product.query.get(int(pid))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price)
                db.session.add(order_item)
        
        order.total_price = total_price
        db.session.commit()
        
        session.pop('cart', None)
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('cart.html', checkout=True)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
