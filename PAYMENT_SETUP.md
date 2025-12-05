# Payment Gateway Setup Guide

This guide will help you configure Stripe and PayPal payment gateways for your e-commerce application.

## Quick Start

### 1. Configure Environment Variables

The `.env` file has been created with placeholders. You need to replace them with your actual test credentials.

### 2. Get Stripe Test Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/register)
2. Create a free account (no credit card required for testing)
3. Navigate to **Developers** → **API keys**
4. Copy your **Publishable key** (starts with `pk_test_`)
5. Copy your **Secret key** (starts with `sk_test_`)
6. Update `.env` file:
   ```
   STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY_HERE
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
   ```

### 3. Get PayPal Sandbox Credentials

1. Go to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. Log in or create a free developer account
3. Go to **Apps & Credentials**
4. Switch to **Sandbox** mode
5. Create a new app or use the default app
6. Copy your **Client ID** and **Secret**
7. Update `.env` file:
   ```
   PAYPAL_CLIENT_ID=YOUR_CLIENT_ID_HERE
   PAYPAL_CLIENT_SECRET=YOUR_SECRET_HERE
   ```

### 4. Restart the Application

After updating the `.env` file, restart both applications:

```powershell
# Stop the running servers (Ctrl+C in each terminal)
# Then restart:
python app.py
python admin.py
```

## Testing Payments

### Stripe Test Cards

Use these test card numbers in Stripe checkout:

- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **Requires Authentication**: `4000 0025 0000 3155`

Use any future expiry date, any 3-digit CVC, and any ZIP code.

### PayPal Sandbox Testing

1. PayPal will provide sandbox test accounts automatically
2. Use the sandbox buyer account credentials to test payments
3. Find test accounts in PayPal Developer Dashboard → **Sandbox** → **Accounts**

## Troubleshooting

### "Stripe API keys not configured" Error

- Ensure your `.env` file has valid Stripe keys
- Keys should start with `pk_test_` and `sk_test_`
- Restart the application after updating `.env`

### PayPal Button Not Working

- Verify `PAYPAL_CLIENT_ID` is set in `.env`
- Ensure you're using Sandbox credentials, not Live
- Check browser console for JavaScript errors

### Changes Not Taking Effect

- Restart both `app.py` and `admin.py`
- Clear browser cache
- Check that `.env` file is in the project root directory

## Security Notes

- ⚠️ Never commit `.env` file to git (it's already in `.gitignore`)
- ⚠️ Never use test keys in production
- ⚠️ Keep your secret keys private

## Need Help?

- [Stripe Documentation](https://stripe.com/docs)
- [PayPal Developer Docs](https://developer.paypal.com/docs/)
- Check `STRIPE_SETUP.md` and `PAYPAL_SETUP.md` for more details
