from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Product, User, Order, OrderItem
import stripe
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
stripe.api_key = app.config['STRIPE_SECRET_KEY']

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
    saved_items_dict = session.get('saved_for_later', {})
    
    products = []
    total_price = 0
    for pid, quantity in cart_items.items():
        product = Product.query.get(int(pid))
        if product:
            total = product.price * quantity
            products.append({'product': product, 'quantity': quantity, 'total': total})
            total_price += total
    
    # Get saved items
    saved_items = []
    for pid, quantity in saved_items_dict.items():
        product = Product.query.get(int(pid))
        if product:
            saved_items.append({'product': product, 'quantity': quantity})
    
    return render_template('cart.html', products=products, total_price=total_price, saved_items=saved_items, paypal_client_id=app.config['PAYPAL_CLIENT_ID'])

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart_items = session.get('cart', {})
    cart_items[str(product_id)] = cart_items.get(str(product_id), 0) + quantity
    session['cart'] = cart_items
    flash('Item added to cart', 'success')
    return redirect(url_for('index'))

@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    action = request.form.get('action')
    cart_items = session.get('cart', {})
    
    if str(product_id) in cart_items:
        if action == 'increase':
            cart_items[str(product_id)] += 1
        elif action == 'decrease':
            cart_items[str(product_id)] -= 1
            if cart_items[str(product_id)] <= 0:
                del cart_items[str(product_id)]
        
        session['cart'] = cart_items
        flash('Cart updated', 'success')
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_items = session.get('cart', {})
    
    if str(product_id) in cart_items:
        del cart_items[str(product_id)]
        session['cart'] = cart_items
        flash('Item removed from cart', 'success')
    
    return redirect(url_for('cart'))

@app.route('/save_for_later/<int:product_id>', methods=['POST'])
def save_for_later(product_id):
    cart_items = session.get('cart', {})
    saved_items = session.get('saved_for_later', {})
    
    if str(product_id) in cart_items:
        quantity = cart_items[str(product_id)]
        saved_items[str(product_id)] = quantity
        del cart_items[str(product_id)]
        
        session['cart'] = cart_items
        session['saved_for_later'] = saved_items
        flash('Item saved for later', 'success')
    
    return redirect(url_for('cart'))

@app.route('/move_to_cart/<int:product_id>', methods=['POST'])
def move_to_cart(product_id):
    cart_items = session.get('cart', {})
    saved_items = session.get('saved_for_later', {})
    
    if str(product_id) in saved_items:
        quantity = saved_items[str(product_id)]
        cart_items[str(product_id)] = cart_items.get(str(product_id), 0) + quantity
        del saved_items[str(product_id)]
        
        session['cart'] = cart_items
        session['saved_for_later'] = saved_items
        flash('Item moved to cart', 'success')
    
    return redirect(url_for('cart'))

@app.route('/remove_from_saved/<int:product_id>', methods=['POST'])
def remove_from_saved(product_id):
    saved_items = session.get('saved_for_later', {})
    
    if str(product_id) in saved_items:
        del saved_items[str(product_id)]
        session['saved_for_later'] = saved_items
        flash('Item removed from saved items', 'success')
    
    return redirect(url_for('cart'))

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

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart_items = session.get('cart', {})
    if not cart_items:
        return redirect(url_for('cart'))

    line_items = []
    for pid, quantity in cart_items.items():
        product = Product.query.get(int(pid))
        if product:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                        'images': [product.image_url] if product.image_url else [],
                    },
                    'unit_amount': int(product.price * 100), # Amount in cents
                },
                'quantity': quantity,
            })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('payment_cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('cart'))

@app.route('/payment/success')
def payment_success():
    session_id = request.args.get('session_id')
    # Verify session if needed, but for now just process order
    
    cart_items = session.get('cart', {})
    if not cart_items:
        return redirect(url_for('index'))

    # Create user/order logic (duplicated from old checkout for now, refactor later)
    user = User.query.first()
    if not user:
        user = User(username='guest', email='guest@example.com')
        db.session.add(user)
        db.session.commit()

    total_price = 0
    order = Order(user_id=user.id, total_price=0, status='Paid') # Status Paid
    db.session.add(order)
    db.session.commit()

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
    flash('Payment successful! Order placed.', 'success')
    return render_template('cart.html', checkout=True)

@app.route('/payment/cancel')
def payment_cancel():
    flash('Payment cancelled.', 'warning')
    return redirect(url_for('cart'))

# PayPal Helpers
def get_paypal_client():
    client_id = app.config['PAYPAL_CLIENT_ID']
    client_secret = app.config['PAYPAL_CLIENT_SECRET']
    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
    return PayPalHttpClient(environment)

@app.route('/api/create-paypal-order', methods=['POST'])
def create_paypal_order():
    cart_items = session.get('cart', {})
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    total_amount = 0
    for pid, quantity in cart_items.items():
        product = Product.query.get(int(pid))
        if product:
            total_amount += product.price * quantity
    
    request = OrdersCreateRequest()
    request.prefer('return=representation')
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "{:.2f}".format(total_amount)
            }
        }]
    })

    try:
        client = get_paypal_client()
        response = client.execute(request)
        return jsonify({'id': response.result.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/capture-paypal-order', methods=['POST'])
def capture_paypal_order():
    data = request.get_json()
    order_id = data.get('orderID')
    
    request = OrdersCaptureRequest(order_id)
    
    try:
        client = get_paypal_client()
        response = client.execute(request)
        
        # Order captured successfully, create local order
        cart_items = session.get('cart', {})
        
        user = User.query.first()
        if not user:
            user = User(username='guest', email='guest@example.com')
            db.session.add(user)
            db.session.commit()

        total_price = 0
        order = Order(user_id=user.id, total_price=0, status='Paid (PayPal)')
        db.session.add(order)
        db.session.commit()

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
        flash('Payment successful! Order placed.', 'success')
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
