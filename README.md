# 🛍️ SEKANI Mall — Django E-Commerce Platform

A full-featured e-commerce platform for SEKANI with Flutterwave escrow payments.

## Features
- Customer registration & SEKANI admin login
- Product listings with images, categories & search/filter
- Shopping cart & checkout
- Flutterwave escrow payments (funds held until OTP delivery confirmed)
- Discount codes (percentage & fixed amount)
- Order tracking with OTP delivery confirmation
- Reviews & dispute system
- SEKANI admin dashboard

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/sekani-mall.git
cd sekani-mall
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env file
```bash
cp .env.example .env
# Fill in your values in .env
```

### 4. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser  # This creates your SEKANI admin
```

### 5. Set the admin role
After creating the superuser, go to Django admin → Users → set role to "SEKANI Admin"

### 6. Run the server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Deploying to Render

1. Push this repo to GitHub
2. Go to render.com → New → Web Service
3. Connect your GitHub repo
4. Render detects render.yaml automatically
5. Add environment variables in Render dashboard
6. Deploy!

## Flutterwave Setup
1. Create account at flutterwave.com
2. Get your API keys from dashboard
3. Add to .env file
4. Set webhook URL in Flutterwave dashboard to: https://yourdomain.com/payments/webhook/

## Admin Login
- Customer login: /accounts/login/
- SEKANI admin login: /accounts/sekani-login/
