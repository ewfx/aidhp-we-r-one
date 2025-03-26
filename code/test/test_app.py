import unittest
import json
from unittest.mock import patch, MagicMock
from app import app, generate_customer_description, generate_product_recommendations

class TestFinanceInsightApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_index_route(self):
        """Test that the index route returns the index.html template"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_get_random_customer_route(self):
        """Test that the get_random_customer route returns customer data"""
        response = self.app.get('/get_random_customer')
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the expected keys
        data = json.loads(response.data)
        self.assertIn('customer', data)
        self.assertIn('persona', data)
        self.assertIn('recommendations', data)
        self.assertIn('admin_data', data)
        
        # Check that customer data contains expected fields
        customer = data['customer']
        self.assertIn('name', customer)
        self.assertIn('age', customer)
        self.assertIn('gender', customer)
        self.assertIn('occupation', customer)
        self.assertIn('salary', customer)
        
        # Check that recommendations are provided
        self.assertTrue(len(data['recommendations']) > 0)
        
    @patch('google.generativeai.GenerativeModel')
    def test_generate_customer_description(self, mock_generative_model):
        """Test the generate_customer_description function"""
        # Mock the Gemini AI response
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a test customer description."
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance
        
        # Test customer data
        customer_data = {
            'name': 'Test User',
            'age': 30,
            'gender': 'Female',
            'marital_status': 'Single',
            'education': 'Bachelor',
            'occupation': 'Engineer',
            'salary': 80000,
            'credit_limit': 10000,
            'credit_utilization': 20,
            'loan_amount': 0,
            'emi_paid': 0,
            'account_balance': 25000,
            'Interest Score': 70,
            'Engagement Score': 65,
            'Sentiment Score': 80,
            'Social Media Activity': 'Medium'
        }
        
        result = generate_customer_description(customer_data)
        
        # Check that the function called the AI model
        mock_model_instance.generate_content.assert_called_once()
        
        # Check that the function returned the expected result
        self.assertEqual(result, "This is a test customer description.")
        
    @patch('google.generativeai.GenerativeModel')
    def test_generate_product_recommendations(self, mock_generative_model):
        """Test the generate_product_recommendations function"""
        # Mock the Gemini AI response
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = """```json
        [
            {
                "name": "Test Credit Card",
                "description": "A credit card for testing",
                "rationale": "This is a good fit because of test reasons"
            },
            {
                "name": "Test Loan",
                "description": "A loan for testing",
                "rationale": "This loan is recommended for test purposes"
            }
        ]
        ```"""
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance
        
        # Test customer data
        customer_data = {
            'name': 'Test User',
            'age': 30,
            'gender': 'Female',
            'marital_status': 'Single',
            'education': 'Bachelor',
            'occupation': 'Engineer',
            'salary': 80000,
            'credit_limit': 10000,
            'credit_utilization': 20,
            'loan_amount': 0,
            'emi_paid': 0,
            'account_balance': 25000,
            'Interest Score': 70,
            'Engagement Score': 65,
            'Sentiment Score': 80,
            'Social Media Activity': 'Medium'
        }
        
        customer_description = "This is a test customer description."
        
        result = generate_product_recommendations(customer_data, customer_description)
        
        # Check that the function called the AI model
        mock_model_instance.generate_content.assert_called_once()
        
        # Check that the function returned the expected structure
        self.assertIn('visible', result)
        self.assertIn('admin_only', result)
        
        # Check that the recommendations were parsed correctly
        self.assertEqual(len(result['visible']), 2)
        self.assertEqual(result['visible'][0]['name'], "Test Credit Card")
        self.assertEqual(result['visible'][1]['name'], "Test Loan")
        
        # Check that the admin insights were parsed correctly
        self.assertEqual(len(result['admin_only']), 2)
        self.assertEqual(result['admin_only'][0], "This is a good fit because of test reasons")
        self.assertEqual(result['admin_only'][1], "This loan is recommended for test purposes")
        
    @patch('app.generate_customer_description')
    @patch('app.generate_product_recommendations')
    def test_get_random_customer_integration(self, mock_recommendations, mock_description):
        """Test the integration of the get_random_customer route with the AI functions"""
        # Mock the AI function responses
        mock_description.return_value = "Test customer description"
        mock_recommendations.return_value = {
            'visible': [
                {'name': 'Test Product 1', 'description': 'Description 1'},
                {'name': 'Test Product 2', 'description': 'Description 2'}
            ],
            'admin_only': [
                'Admin insight 1',
                'Admin insight 2'
            ]
        }
        
        response = self.app.get('/get_random_customer')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Check that the AI-generated content is included in the response
        self.assertEqual(data['persona'], "Test customer description")
        self.assertEqual(len(data['recommendations']), 2)
        self.assertEqual(data['recommendations'][0]['name'], 'Test Product 1')
        self.assertEqual(len(data['admin_data']), 2)
        self.assertEqual(data['admin_data'][0], 'Admin insight 1')

if __name__ == '__main__':
    unittest.main()

