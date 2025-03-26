from flask import Flask, render_template, request, jsonify
import random
import json
import os
import pandas as pd
import requests
from io import StringIO
from sklearn.preprocessing import StandardScaler
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini AI
# In a production environment, you would store this in environment variables
GEMINI_API_KEY = "AIzaSyBL_TVeqisn773sbtPHFF90qzEQwlwH4-A"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# URLs for CSV files - update these to your actual paths
CUSTOMER_DATA_CSV_URL = "Customer_DB/Customer_Data_with_Social_Media_Activity.csv"
WELLS_FARGO_PRODUCTS_CSV_URL = "Product_DB/Wells_Fargo_Products_Full.csv"

# Load Wells Fargo products data
def load_wells_fargo_products():
    try:
        # Check if file exists locally
        if os.path.exists(WELLS_FARGO_PRODUCTS_CSV_URL):
            products_df = pd.read_csv(WELLS_FARGO_PRODUCTS_CSV_URL)
        else:
            # Try to fetch from URL if not local
            response = requests.get(WELLS_FARGO_PRODUCTS_CSV_URL)
            response.raise_for_status()
            products_df = pd.read_csv(StringIO(response.text))
        
        # Convert DataFrame to list of dictionaries for easier use
        products_list = products_df.to_dict(orient='records')
        
        print(f"Successfully loaded {len(products_list)} Wells Fargo products")
        return products_list
    except Exception as e:
        print(f"Error loading Wells Fargo products: {e}")
        # Return a minimal fallback dataset if loading fails
        return [
            {"Card Name": "Basic Credit Card", "Annual Fee": "$0", "Benefits": "Cash back rewards", "Ideal For": "Everyday spending", "Loan Type": ""},
            {"Card Name": "", "Annual Fee": "", "Benefits": "Low interest rates", "Ideal For": "Home buyers", "Loan Type": "Home Loan"}
        ]

# Load customer data from CSV
def load_customer_data():
    try:
        # Check if file exists locally
        if os.path.exists(CUSTOMER_DATA_CSV_URL):
            print(f"Loading customer data from local file: {CUSTOMER_DATA_CSV_URL}")
            customers_df = pd.read_csv(CUSTOMER_DATA_CSV_URL)
        else:
            # Try to fetch from URL if not local
            print(f"Attempting to load customer data from URL: {CUSTOMER_DATA_CSV_URL}")
            response = requests.get(CUSTOMER_DATA_CSV_URL)
            response.raise_for_status()
            customers_df = pd.read_csv(StringIO(response.text))
        
        # Convert DataFrame to list of dictionaries
        customers_list = customers_df.to_dict(orient='records')
        
        # Add transaction history to each customer
        for customer in customers_list:
            customer['transaction_history'] = generate_sample_transactions()
            
        print(f"Successfully loaded {len(customers_list)} customers from database")
        return customers_list
    except Exception as e:
        print(f"Error loading customer data: {e}")
        print("Falling back to sample customer data")
        # Return sample data if loading fails
        return generate_sample_customers()

# Generate sample transactions for demo purposes
def generate_sample_transactions():
    categories = ["Groceries", "Dining", "Rent", "Mortgage", "Utilities", "Shopping", "Travel", "Entertainment", "Salary"]
    transactions = []
    
    # Generate 4-8 random transactions
    for i in range(random.randint(4, 8)):
        is_income = random.random() < 0.25  # 25% chance of being income
        category = "Salary" if is_income else random.choice([c for c in categories if c != "Salary"])
        amount = random.randint(1000, 5000) if is_income else -random.randint(20, 2000)
        
        # Generate date (more recent transactions first)
        month = 3  # March
        day = 15 - i  # Starting from the 15th and going back
        if day < 1:
            month -= 1
            day = 28 + day  # Wrap to previous month
            
        transactions.append({
            "date": f"2023-{month:02d}-{day:02d}",
            "amount": amount,
            "category": category
        })
    
    return transactions

# Generate sample customers for fallback
def generate_sample_customers():
    print("Generating sample customer data as fallback")
    return [
        {
            "customer_id": 1,
            "name": "John Smith",
            "age": 35,
            "gender": "Male",
            "marital_status": "Married",
            "education": "Bachelor",
            "occupation": "Software Engineer",
            "salary": 95000,
            "loan_amount": 150000,
            "credit_limit": 15000,
            "credit_utilization": 25,
            "emi_paid": 2000,
            "tenure_months": 60,
            "max_dpd": 0,
            "default_status": 0,
            "product_type": "Home Loan",
            "enquiry_amount": 5000,
            "unique_products_enquired": 2,
            "total_enquiries": 3,
            "transaction_amount": 8500,
            "account_balance": 45000,
            "is_salary": 1,
            "Credit Card": 1,
            "Home Loan": 1,
            "Personal Loan": 0,
            "Interest Score": 75,
            "Engagement Score": 82,
            "Sentiment Score": 68,
            "Social Media Activity": "High",
            "transaction_history": generate_sample_transactions()
        },
        # Additional sample customers...
    ]

# Load data at startup
print("Initializing application data...")
wells_fargo_products = load_wells_fargo_products()
customers = load_customer_data()
print(f"Initialization complete. Loaded {len(customers)} customers and {len(wells_fargo_products)} products.")

# Rest of the application code...
# (generate_customer_description, generate_product_recommendations, routes, etc.)

