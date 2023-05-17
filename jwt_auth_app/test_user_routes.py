import unittest
from flask import Flask
from main import app, db
from database import create_database

class AdminViewTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask application
        self.app = app

        # Set up a test client
        self.client = self.app.test_client()

        # Create the test database tables
        with self.app.app_context():
            create_database()
        
        response = self.client.post('/login', json={
            'username': 'admin@example.com',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 200)
        self.access_token = response.json['token']

        # Set the headers with the access token
        self.headers = {'Authorization': f'Bearer {self.access_token}'}

    def test_create_admin(self):
        Send a POST request to create an admin user
        response = self.client.post('/admin/create', data={
            'email': 'admin@example.com',
            'password': 'admin123'
        })

        # Assert that the response has the expected status code
        # self.assertEqual(response.status_code, 201)

        response = self.client.post('/login', json={
            'username': 'admin11@example.com',
            'password': 'admin123'
            })
        self.assertEqual(response.status_code, 200)
        self.access_token = response.json['token']
        self.headers = {'Authorization': 'Bearer ' + self.access_token}
    
    def test_get_user(self):
        # Send a GET request to retrieve a user with authentication headers
        response = self.client.get('/users/1', headers=self.headers)

        # Assert that the response has the expected status code
        self.assertEqual(response.status_code, 200)

        # Assert that the user data in the response is correct

    def test_update_user(self):
        # Send a PUT request to update a user with authentication headers
        response = self.client.put('/users/1', json={
            'email': 'newemail@example.com'
        }, headers=self.headers)

        # Assert that the response has the expected status code
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
