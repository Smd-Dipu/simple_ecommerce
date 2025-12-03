# Stripe Integration Setup Guide

This guide will help you set up Stripe payment processing for the e-commerce application.

## Prerequisites

- A computer with internet access
- An email address
- No credit card required for test mode!

## Step 1: Create a Stripe Account

1. Go to [Stripe.com](https://stripe.com/)
2. Click **"Start now"** or **"Sign up"**
3. Fill in your information:
   - Email address
   - Full name
   - Country
   - Password
4. Click **"Create account"**
5. Verify your email address by clicking the link sent to your inbox

> [!NOTE]
> You can start testing immediately without providing business details or bank information. Stripe allows you to use test mode right away.

## Step 2: Access Your Test API Keys

1. Log in to your [Stripe Dashboard](https://dashboard.stripe.com/)
2. You'll see a toggle in the top-right that says **"Test mode"** - make sure it's ON (it should be by default)
3. In the left sidebar, click **"Developers"**
4. Click **"API keys"**

You'll see two types of keys:

### Publishable Key (Public)
- Starts with `pk_test_`
- Safe to use in client-side code
- Example: `pk_test_51Abc123...`

### Secret Key (Private)
- Starts with `sk_test_`
- Click **"Reveal test key"** to see it
- **NEVER share this or commit it to version control!**
- Example: `sk_test_51Abc123...`

## Step 3: Configure Your Application

You have two options for configuring your Stripe keys:

### Option A: Using Environment Variables (Recommended)

1. **Create a `.env` file** in your project root:
   ```bash
   cd e:\Programming\Antigravity\simple_ecommerce
   copy .env.example .env
   ```

2. **Edit the `.env` file** and add your actual keys:
   ```
   STRIPE_PUBLIC_KEY=pk_test_YOUR_ACTUAL_KEY_HERE
   STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_KEY_HERE
   ```

3. **Save the file**

> [!IMPORTANT]
> The `.env` file is already in `.gitignore`, so it won't be committed to version control.

### Option B: Direct Configuration (For Testing Only)

Edit `config.py` and replace the placeholder values:

```python
# Stripe Configuration
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_YOUR_ACTUAL_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_YOUR_ACTUAL_KEY')
```

> [!WARNING]
> If you use Option B, be careful not to commit your actual keys to Git!

## Step 4: Test Your Integration

### Start the Application

```bash
cd e:\Programming\Antigravity\simple_ecommerce
python app.py
```

### Test the Payment Flow

1. Open your browser to `http://localhost:5000`
2. Browse products and add items to your cart
3. Go to the cart page
4. Click **"Pay with Card"**
5. You'll be redirected to Stripe's checkout page

### Use Test Card Numbers

Stripe provides test card numbers for different scenarios:

#### Successful Payment
- **Card Number**: `4242 4242 4242 4242`
- **Expiry**: Any future date (e.g., `12/34`)
- **CVC**: Any 3 digits (e.g., `123`)
- **ZIP**: Any 5 digits (e.g., `12345`)

#### Card Declined
- **Card Number**: `4000 0000 0000 0002`
- Use same expiry, CVC, and ZIP as above

#### Insufficient Funds
- **Card Number**: `4000 0000 0000 9995`

#### Requires 3D Secure Authentication
- **Card Number**: `4000 0025 0000 3155`

> [!TIP]
> Find more test cards at [Stripe's Testing Documentation](https://stripe.com/docs/testing)

### Verify the Payment

After completing a test payment:

1. **In Your Application**:
   - You should see a success message
   - Your cart should be empty
   - The order should be in your database

2. **In Stripe Dashboard**:
   - Go to [Payments → All payments](https://dashboard.stripe.com/test/payments)
   - You should see your test payment listed
   - Click on it to see details

## Step 5: View Payment History

1. Log in to your [Stripe Dashboard](https://dashboard.stripe.com/)
2. Make sure **"Test mode"** is ON
3. Click **"Payments"** in the left sidebar
4. You'll see all your test payments

You can:
- View payment details
- See customer information
- Check payment status
- Issue refunds (in test mode)

## Troubleshooting

### "Invalid API Key" Error

**Problem**: The application shows an error about invalid API keys.

**Solutions**:
- Double-check you copied the entire key (they're quite long)
- Make sure you're using **test** keys (starting with `pk_test_` and `sk_test_`)
- Verify there are no extra spaces before or after the keys
- Restart the application after changing configuration

### "No such checkout session" Error

**Problem**: Payment success page shows an error.

**Solution**: This usually means the session verification failed. Make sure you're using the latest version of the code with proper session verification.

### Checkout Page Doesn't Load

**Problem**: Clicking "Pay with Card" doesn't redirect to Stripe.

**Solutions**:
- Check browser console for JavaScript errors
- Verify your secret key is configured correctly
- Make sure the cart is not empty
- Check server logs for error messages

### Payment Succeeds but Order Not Created

**Problem**: Payment completes in Stripe but no order in database.

**Solutions**:
- Check server logs for database errors
- Verify the database is initialized (`app.db` exists)
- Make sure at least one user exists in the database

## Going to Production

When you're ready to accept real payments:

### 1. Activate Your Stripe Account

1. In Stripe Dashboard, click **"Activate your account"**
2. Provide business information
3. Add bank account details for payouts
4. Complete identity verification

### 2. Get Live API Keys

1. Toggle **"Test mode"** to OFF in the dashboard
2. Go to **Developers → API keys**
3. Copy your **Live** keys (starting with `pk_live_` and `sk_live_`)

### 3. Update Configuration

Update your production environment variables:
```
STRIPE_PUBLIC_KEY=pk_live_YOUR_LIVE_KEY
STRIPE_SECRET_KEY=sk_live_YOUR_LIVE_KEY
```

> [!CAUTION]
> **Never use live keys in development!** Always keep test and live keys separate.

### 4. Set Up Webhooks (Recommended)

For production, set up webhooks to handle:
- Payment confirmations
- Failed payments
- Refunds
- Disputes

See [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks) for details.

## Additional Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Checkout Guide](https://stripe.com/docs/payments/checkout)
- [Stripe Testing Guide](https://stripe.com/docs/testing)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Support](https://support.stripe.com/)

## Security Best Practices

1. ✅ **Never commit API keys to version control**
2. ✅ **Use environment variables for configuration**
3. ✅ **Keep test and live keys separate**
4. ✅ **Verify webhook signatures in production**
5. ✅ **Use HTTPS in production**
6. ✅ **Regularly rotate your API keys**
7. ✅ **Monitor your Stripe dashboard for suspicious activity**

## Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review Stripe's [testing documentation](https://stripe.com/docs/testing)
3. Check server logs for detailed error messages
4. Visit [Stripe's support center](https://support.stripe.com/)
