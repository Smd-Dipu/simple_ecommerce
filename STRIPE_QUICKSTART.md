# Quick Start: Testing Stripe Checkout

## 🚀 Fast Track (5 Minutes)

### 1. Get Stripe Keys (2 minutes)
1. Go to https://dashboard.stripe.com/register
2. Sign up (no credit card needed)
3. Click **Developers** → **API keys**
4. Copy both test keys

### 2. Configure (1 minute)
Edit `config.py` lines 15-16:
```python
STRIPE_PUBLIC_KEY = 'pk_test_YOUR_KEY_HERE'
STRIPE_SECRET_KEY = 'sk_test_YOUR_KEY_HERE'
```

### 3. Test (2 minutes)
```bash
# Start app
python app.py

# Open browser to http://localhost:5000
# Add items to cart
# Click "Pay with Card"
# Use card: 4242 4242 4242 4242
# Expiry: 12/34, CVC: 123, ZIP: 12345
```

## ✅ Success Checklist
- [ ] Redirected to Stripe checkout page
- [ ] Payment completes successfully
- [ ] Redirected back to success page
- [ ] Cart is empty
- [ ] Order appears in database

## 📚 Full Documentation
See [STRIPE_SETUP.md](file:///e:/Programming/Antigravity/simple_ecommerce/STRIPE_SETUP.md) for complete guide.

## 🧪 Test Cards

| Scenario | Card Number |
|----------|-------------|
| ✅ Success | 4242 4242 4242 4242 |
| ❌ Declined | 4000 0000 0000 0002 |
| 💰 Insufficient Funds | 4000 0000 0000 9995 |
| 🔐 3D Secure | 4000 0025 0000 3155 |

All cards: Expiry: any future date, CVC: any 3 digits, ZIP: any 5 digits
