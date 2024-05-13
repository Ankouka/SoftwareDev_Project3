from app import db 
from flask_login import UserMixin

user_soulmates = db.Table('user_soulmates', 
                          db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('soulmate_id', db.Integer, db.ForeignKey('soulmates.id'), primary_key=True)
                         )

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    passwd = db.Column(db.String)
    soulmates = db.relationship('Soulmate', secondary=user_soulmates, backref=db.backref('users', lazy=True))

class User_Profile(db.Model, UserMixin):
    __tablename__ = 'user_profiles'
    profile_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    preference = db.Column(db.String)
    bio = db.Column(db.String)
    occupation = db.Column(db.String)
    picture = db.Column(db.String)
    age = db.Column(db.String)
    sex = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))  # Foreign key relationship

    user = db.relationship('User', backref='profile')  # Define the relationship to User
    user_id = db.Column(db.String, db.ForeignKey('users.id'))  # Foreign key relationship
    user = db.relationship('User', backref='profile')

class Soulmate(db.Model):
    __tablename__ = 'soulmates'
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.String, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    bio = db.Column(db.String)
    pic = db.Column(db.String)

    #user = db.relationship('User', foreign_keys=[user_id], backref='soulmate')
    #soulmate = db.relationship('User', foreign_keys=[soulmate_id], backref='soulmate')



class Message(db.Model):
    message_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    recipient = db.Column(db.String)
    text = db.Column(db.String)
    time = db.Column(db.DateTime)
