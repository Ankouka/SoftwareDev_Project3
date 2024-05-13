import unittest
from unittest.mock import patch
from app import app
from app.models import User

class TestProfileUpdateEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.current_user', new_callable=lambda: User(id='test_user_id'))
    def test_profile_update(self, current_user):
        with app.test_client() as client:
            
            response = client.post('/users/edit profile', data={
                'name': 'New Name',
            })
            self.assertEqual(response.status_code, 200)