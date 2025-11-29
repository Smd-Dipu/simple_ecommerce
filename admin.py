from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Order, User
from sqlalchemy import func
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models import db, Order, User

# ... (imports)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # Allow admin or staff
        if user and user.is_admin and user.password_hash == password:
            session['admin_user_id'] = user.id
            session['admin_role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('admin_user_id', None)
    session.pop('admin_role', None)
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['admin_user_id'])
    return render_template('admin_profile.html', user=user)

@app.route('/users')
@login_required
def users():
    # Only admin can manage users
    if session.get('admin_role') != 'admin':
        flash('Access denied. Admin role required.', 'danger')
        return redirect(url_for('dashboard'))
        
    all_users = User.query.all()
    return render_template('admin_users.html', users=all_users)

@app.route('/update-role/<int:user_id>', methods=['POST'])
@login_required
def update_role(user_id):
    if session.get('admin_role') != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role in ['admin', 'staff', 'customer']:
        user.role = new_role
        # Sync is_admin flag for backward compatibility/simplicity
        user.is_admin = (new_role in ['admin', 'staff'])
        db.session.commit()
        flash(f'Role updated for {user.username}', 'success')
    
    return redirect(url_for('users'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user = User.query.get(session['admin_user_id'])
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if user.password_hash != current_password:
        flash('Incorrect current password', 'danger')
        return redirect(url_for('profile'))
        
    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('profile'))
        
    user.password_hash = new_password
    db.session.commit()
    
    flash('Password updated successfully', 'success')
    return redirect(url_for('profile'))

@app.route('/')
@login_required
def dashboard():
    # Recent transactions
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Sales chart data (Last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # SQLite specific date extraction
    sales_data = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_price).label('total')
    ).filter(Order.created_at >= thirty_days_ago)\
    .group_by(func.date(Order.created_at))\
    .order_by(func.date(Order.created_at)).all()
    
    dates = [data.date for data in sales_data]
    totals = [data.total for data in sales_data]
    
    return render_template('admin.html', orders=recent_orders, dates=dates, totals=totals)

if __name__ == '__main__':
    with app.app_context():
        # Ensure DB exists (though app.py should have created it)
        db.create_all()
    app.run(debug=True, port=5001)
