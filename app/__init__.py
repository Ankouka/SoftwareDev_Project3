from flask import Flask
import os
import json

app = Flask("Queen Soopers Web App")
app.secret_key = os.environ['SECRET_KEY']

# Import SQLAlchemy and initialize the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

# Import your models and define relationships
from app.models import User, Soulmate

# Define a function to add initial soulmates from the JSON file
def add_initial_soulmates():
    Soulmate.query.delete()
    with open('static/profiles.json', 'r') as file:
        soulmates_data = json.load(file)

    for soulmate_data in soulmates_data:
        soulmate = Soulmate(**soulmate_data)
        db.session.add(soulmate)

    db.session.commit()

# Create the app context and initialize the database
with app.app_context(): 
    db.create_all()
    add_initial_soulmates()

# Setup the login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

# Import routes (assuming your routes are in a separate file)
from app import routes
