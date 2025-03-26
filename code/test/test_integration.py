import unittest
import requests
import json
import time

class TestFinanceInsightIntegration(unittest.TestCase):
    """Integration tests for the FinanceInsight Bank application.
    
    These tests assume the Flask application is running on http://localhost:5000.
    Start the application with `python app.py` before running these tests.
    """
    
    BASE_URL = "http://localhost:5000"
    
    def setUp(self):
        # Wait a moment to ensure the server is ready
        time.sleep(1)
    
    def test_index_page_loads(self):
        """Test that the index page loads successfully"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("FinanceInsight Bank", response.text)
        
    def test_get_random_customer_api(self):
        """Test that the get_random_customer API returns valid data"""
        response = requests.get(f"{self.BASE_URL}/get_random_customer")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Check that the response contains the expected keys
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
        
    def test_response_time(self):
        """Test that the API responds within a reasonable time frame"""
        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/get_random_customer")
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        
        # Response should come back in less than 10 seconds
        # Note: This might need adjustment based on your AI model's response time
        response_time = end_time - start_time
        self.assertLess(response_time, 10, f"Response time was {response_time} seconds")
        
    def test_multiple_requests(self):
        """Test that multiple requests return different customers"""
        response1 = requests.get(f"{self.BASE_URL}/get_random_customer")
        response2 = requests.get(f"{self.BASE_URL}/get_random_customer")
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        
        data1 = response1.json()
        data2 = response2.json()
        
        # There's a small chance this could fail if the same customer is randomly selected twice
        # But with enough customers in the database, this should be rare
        customer_id1 = data1['customer'].get('customer_id')
        customer_id2 = data2['customer'].get('customer_id')
        
        # If we got the same customer twice, try one more time
        if customer_id1 == customer_id2:
            response3 = requests.get(f"{self.BASE_URL}/get_random_customer")
            self.assertEqual(response3.status_code, 200)
            data3 = response3.json()
            customer_id3 = data3['customer'].get('customer_id')
            
            # At least one of the three requests should be different
            self.assertTrue(
                customer_id1 != customer_id2 or 
                customer_id1 != customer_id3 or 
                customer_id2 != customer_id3,
                "Multiple requests returned the same customer"
            )

if __name__ == '__main__':
    unittest.main()

