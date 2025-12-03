# PayPal Integration Setup Guide

This guide will help you set up PayPal payment gateway integration for the e-commerce application.

## Prerequisites

- PayPal Developer Account
- Python environment with all dependencies installed

## Step 1: Create PayPal Developer Account

1. Go to [PayPal Developer Portal](https://developer.paypal.com/)
2. Click **"Log in to Dashboard"** or **"Sign Up"**
3. Use your existing PayPal account or create a new one
4. Complete the registration process

## Step 2: Create a Sandbox Application

1. Once logged in, navigate to **Dashboard** → **My Apps & Credentials**
2. Make sure you're in **Sandbox** mode (toggle at the top)
3. Click **"Create App"** button
4. Enter an app name (e.g., "My E-commerce Store")
5. Click **"Create App"**

## Step 3: Get Your API Credentials

After creating the app, you'll see:

- **Client ID**: A long string starting with `A...`
- **Secret**: Click "Show" to reveal it

**Important**: Keep these credentials secure and never commit them to version control!

## Step 4: Configure Your Application

### Option A: Using Environment Variables (Recommended)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   PAYPAL_CLIENT_ID=your-actual-client-id-here
   PAYPAL_CLIENT_SECRET=your-actual-secret-here
   ```

3. Make sure `.env` is in your `.gitignore` file

### Option B: Direct Configuration (Not Recommended for Production)

Edit `config.py` and replace the placeholder values:

```python
PAYPAL_CLIENT_ID = 'your-actual-client-id-here'
PAYPAL_CLIENT_SECRET = 'your-actual-secret-here'
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Test the Integration

### Create Sandbox Test Accounts

1. In PayPal Developer Dashboard, go to **Sandbox** → **Accounts**
2. You'll see default test accounts (Personal and Business)
3. Note the email and password for the **Personal** account (this is your test buyer)

### Test Payment Flow

1. Start your application:
   ```bash
   python app.py
   ```

2. Open browser to `http://localhost:5000`

3. Add items to cart and proceed to checkout

4. Click the **PayPal** button

5. Log in with your **Sandbox Personal Account** credentials

6. Complete the payment

7. Verify the order appears in your database with status "Paid (PayPal)"

## Switching to Production

When you're ready to go live:

1. Go to PayPal Developer Dashboard
2. Switch from **Sandbox** to **Live** mode (toggle at top)
3. Create a new Live app or use existing one
4. Get your **Live** Client ID and Secret
5. Update your environment variables with Live credentials
6. Update `app.py` line 265 to use `LiveEnvironment` instead of `SandboxEnvironment`:

```python
from paypalcheckoutsdk.core import PayPalHttpClient, LiveEnvironment

def get_paypal_client():
    client_id = app.config['PAYPAL_CLIENT_ID']
    client_secret = app.config['PAYPAL_CLIENT_SECRET']
    environment = LiveEnvironment(client_id=client_id, client_secret=client_secret)
    return PayPalHttpClient(environment)
```

## Troubleshooting

### PayPal Button Not Showing

- Check browser console for JavaScript errors
- Verify `PAYPAL_CLIENT_ID` is set correctly
- Make sure the cart is not empty

### "Invalid Client ID" Error

- Double-check your Client ID is copied correctly
- Ensure you're using Sandbox credentials with SandboxEnvironment
- Verify no extra spaces in the credential strings

### Payment Not Completing

- Check server logs for errors
- Verify your Secret is correct
- Ensure the capture endpoint is accessible

### Orders Not Saving to Database

- Check that the database is properly initialized
- Verify the User table has at least one user (guest user is auto-created)
- Check server logs for database errors

## Additional Resources

- [PayPal Developer Documentation](https://developer.paypal.com/docs/)
- [PayPal Checkout Integration Guide](https://developer.paypal.com/docs/checkout/)
- [PayPal SDK for Python](https://github.com/paypal/Checkout-Python-SDK)

## Support

For PayPal-specific issues, visit the [PayPal Developer Community](https://www.paypal-community.com/t5/Developer-Community/ct-p/developer-community)
