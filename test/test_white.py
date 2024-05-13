import unittest
from app import app, db
from app.models import User_Profile

class TestProfileCreation(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_profile(self):
        with app.app_context():
            new_profile = User_Profile(name="Test User", preference="Testing")
            db.session.add(new_profile)
            db.session.commit()

            created_profile = User_Profile.query.filter_by(name="Test User").first()
            self.assertIsNotNone(created_profile)





            