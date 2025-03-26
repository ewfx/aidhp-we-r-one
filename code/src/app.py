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

# URLs for CSV files
CUSTOMER_DATA_CSV_URL = "Customer_DB/Customer_Data_with_Social_Media_Activity.csv"  # Replace with your actual CSV path
WELLS_FARGO_PRODUCTS_CSV_URL = "Product_DB/Wells_Fargo_Products_Full.csv"

# Load Wells Fargo products data
def load_wells_fargo_products():
  try:
    #   response = requests.get(WELLS_FARGO_PRODUCTS_CSV_URL)
    #   response.raise_for_status()  # Raise an exception for HTTP errors
      
      # Read CSV from the response content
      products_df = pd.read_csv(WELLS_FARGO_PRODUCTS_CSV_URL)
      
      # Convert DataFrame to list of dictionaries for easier use
      products_list = products_df.to_dict(orient='records')
      
      print(f"Loaded {len(products_list)} Wells Fargo products")
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
      # For local file
      if os.path.exists(CUSTOMER_DATA_CSV_URL):
          customers_df = pd.read_csv(CUSTOMER_DATA_CSV_URL)
      else:
          # For remote file
          response = requests.get(CUSTOMER_DATA_CSV_URL)
          response.raise_for_status()
          customers_df = pd.read_csv(StringIO(response.text))
      
      # Convert DataFrame to list of dictionaries
      customers_list = customers_df.to_dict(orient='records')
      
      # Add transaction history to each customer (this would ideally come from another data source)
      for customer in customers_list:
          customer['transaction_history'] = generate_sample_transactions()
          
      print(f"Loaded {len(customers_list)} customers")
      return customers_list
  except Exception as e:
      print(f"Error loading customer data: {e}")
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
      {
          "customer_id": 2,
          "name": "Sarah Johnson",
          "age": 42,
          "gender": "Female",
          "marital_status": "Divorced",
          "education": "Master",
          "occupation": "Marketing Director",
          "salary": 110000,
          "loan_amount": 0,
          "credit_limit": 25000,
          "credit_utilization": 10,
          "emi_paid": 0,
          "tenure_months": 0,
          "max_dpd": 0,
          "default_status": 0,
          "product_type": "Credit Card",
          "enquiry_amount": 30000,
          "unique_products_enquired": 1,
          "total_enquiries": 1,
          "transaction_amount": 12500,
          "account_balance": 75000,
          "is_salary": 1,
          "Credit Card": 1,
          "Home Loan": 0,
          "Personal Loan": 0,
          "Interest Score": 92,
          "Engagement Score": 88,
          "Sentiment Score": 85,
          "Social Media Activity": "Medium",
          "transaction_history": generate_sample_transactions()
      },
      {
          "customer_id": 3,
          "name": "Michael Chen",
          "age": 28,
          "gender": "Male",
          "marital_status": "Single",
          "education": "Bachelor",
          "occupation": "Graphic Designer",
          "salary": 65000,
          "loan_amount": 25000,
          "credit_limit": 8000,
          "credit_utilization": 40,
          "emi_paid": 500,
          "tenure_months": 36,
          "max_dpd": 15,
          "default_status": 0,
          "product_type": "Personal Loan",
          "enquiry_amount": 10000,
          "unique_products_enquired": 3,
          "total_enquiries": 5,
          "transaction_amount": 4500,
          "account_balance": 12000,
          "is_salary": 1,
          "Credit Card": 1,
          "Home Loan": 0,
          "Personal Loan": 1,
          "Interest Score": 65,
          "Engagement Score": 45,
          "Sentiment Score": 72,
          "Social Media Activity": "Low",
          "transaction_history": generate_sample_transactions()
      }
  ]

# Load data at startup
customers = load_customer_data()
wells_fargo_products = load_wells_fargo_products()

# Update the generate_customer_description function to include the new metrics
def generate_customer_description(customer_data):
  """Generate a detailed customer profile using Gemini AI"""
  try:
      # Create a prompt with customer data
      prompt = f"""
      Generate a detailed customer profile based on the following data:
      
      Name: {customer_data['name']}
      Age: {customer_data['age']}
      Gender: {customer_data['gender']}
      Marital Status: {customer_data['marital_status']}
      Education: {customer_data['education']}
      Occupation: {customer_data['occupation']}
      Income: ${customer_data['salary']}
      Credit Score: {customer_data.get('credit_score', 'Not available')}
      Credit Limit: ${customer_data['credit_limit']}
      Credit Utilization: {customer_data['credit_utilization']}%
      Loan Amount: ${customer_data['loan_amount']}
      EMI Paid: ${customer_data['emi_paid']}
      Account Balance: ${customer_data['account_balance']}
      
      Customer Engagement Metrics:
      Interest Score: {customer_data.get('Interest Score', 'Not available')}/100
      Engagement Score: {customer_data.get('Engagement Score', 'Not available')}/100
      Sentiment Score: {customer_data.get('Sentiment Score', 'Not available')}/100
      Social Media Activity: {customer_data.get('Social Media Activity', 'Not available')}
      Last Social Media Activity: {customer_data.get('Last Social Media Activity', 'Not available')}
      
      Provide a comprehensive financial profile that includes spending habits, financial goals, 
      risk tolerance, and potential financial needs. Focus on their current financial situation,
      their engagement with banking services, and what products might benefit them based on their
      interest and sentiment scores. Consider Social Media Activity and Last Social Media Activity 
      fields as key fields, and provide a recommendation based on it.
      """
      
      # Call Gemini AI to generate the description
      model = genai.GenerativeModel("gemini-1.5-pro-latest")
      response = model.generate_content(prompt)
      
      return response.text
  except Exception as e:
      print(f"Error generating customer description: {e}")
      return "Unable to generate customer description at this time."

# Update the generate_product_recommendations function to consider the new metrics
def generate_product_recommendations(customer_data, customer_description):
  """Generate personalized product recommendations using Gemini AI and Wells Fargo products data"""
  try:
      # Format Wells Fargo products for the prompt
      products_context = ""
      for product in wells_fargo_products:
          if product.get("Card Name"):
              products_context += f"Credit Card: {product.get('Card Name', 'N/A')}\n"
              products_context += f"Annual Fee: {product.get('Annual Fee', 'N/A')}\n"
              products_context += f"Benefits: {product.get('Benefits', 'N/A')}\n"
              products_context += f"Ideal For: {product.get('Ideal For', 'N/A')}\n\n"
          elif product.get("Loan Type"):
              products_context += f"Loan: {product.get('Loan Type', 'N/A')}\n"
              products_context += f"Benefits: {product.get('Benefits', 'N/A')}\n"
              products_context += f"Ideal For: {product.get('Ideal For', 'N/A')}\n\n"
      
      # Create a prompt for product recommendations
      prompt = f"""
      Based on the following customer profile and available Wells Fargo financial products, 
      recommend 3-5 suitable products that would best meet this customer's needs, and one of 
      them based on the social media parameters
      
      Customer Profile:
      {customer_description}
      
      Additional Customer Data:
      - Age: {customer_data['age']}
      - Gender: {customer_data['gender']}
      - Marital Status: {customer_data['marital_status']}
      - Education: {customer_data['education']}
      - Occupation: {customer_data['occupation']}
      - Income: ${customer_data['salary']}
      - Credit Utilization: {customer_data['credit_utilization']}%
      - Loan Amount: ${customer_data['loan_amount']}
      - Account Balance: ${customer_data['account_balance']}
      - Current Products: {', '.join([k for k in ['Credit Card', 'Home Loan', 'Personal Loan'] if customer_data.get(k) == 1])}
      
      Customer Engagement Metrics:
      - Interest Score: {customer_data.get('Interest Score', 'Not available')}/100
      - Engagement Score: {customer_data.get('Engagement Score', 'Not available')}/100
      - Sentiment Score: {customer_data.get('Sentiment Score', 'Not available')}/100
      - Social Media Activity: {customer_data.get('Social Media Activity', 'Not available')}
      - Last Social Media Activity: {customer_data.get('Last Social Media Activity', 'Not available')}
      
      Available Wells Fargo Products:
      {products_context}
      
      For each recommended product:
      1. Provide the exact product name from the list above
      2. A brief description of why it's specifically suitable for this customer
      3. How it addresses their financial needs or goals
      4. How it aligns with their engagement metrics and sentiment
      
      Format as a JSON array of objects with "name", "description", and "rationale" fields.
      """
      
      # Call Gemini AI to generate recommendations
      model = genai.GenerativeModel("gemini-1.5-pro-latest")
      response = model.generate_content(prompt)
      
      # Parse the response to extract recommendations
      try:
          # Try to parse as JSON
          recommendations_text = response.text
          # Find JSON content between triple backticks if present
          import re
          json_match = re.search(r'\`\`\`json\s*([\s\S]*?)\s*\`\`\`', recommendations_text)
          if json_match:
              recommendations_text = json_match.group(1)
          
          recommendations_list = json.loads(recommendations_text)
          
          # Format recommendations for the UI
          visible_recommendations = []
          for rec in recommendations_list:
              visible_recommendations.append({
                  "name": rec["name"],
                  "description": rec["description"]
              })
          
          # Generate admin insights
          admin_insights = []
          for rec in recommendations_list:
              if "rationale" in rec:
                  admin_insights.append(rec["rationale"])
          
          return {
              "visible": visible_recommendations,
              "admin_only": admin_insights
          }
      except Exception as e:
          print(f"Error parsing recommendations: {e}")
          # Fallback to default recommendations
          return {
              "visible": [
                  {"name": "Savings Account", "description": "Basic savings account with competitive interest rates"},
                  {"name": "Credit Card", "description": "Standard credit card with rewards program"}
              ],
              "admin_only": [
                  "AI recommendation parsing failed, showing default recommendations",
                  f"Error details: {str(e)}"
              ]
          }
          
  except Exception as e:
      print(f"Error generating product recommendations: {e}")
      return {
          "visible": [
              {"name": "Savings Account", "description": "Basic savings account with competitive interest rates"}
          ],
          "admin_only": [
              "Unable to generate AI recommendations at this time.",
              f"Error details: {str(e)}"
          ]
      }

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_random_customer')
def get_random_customer():
  customer = random.choice(customers)
  
  # Generate AI-powered customer description
  ai_description = generate_customer_description(customer)
  
  # Generate AI-powered product recommendations
  ai_recommendations = generate_product_recommendations(customer, ai_description)
  
  response = {
      'customer': customer,
      'persona': ai_description,  # Use AI-generated description
      'recommendations': ai_recommendations['visible'],  # Use AI-generated recommendations
      'admin_data': ai_recommendations['admin_only']
  }
  
  return jsonify(response)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)

