from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email_address = StringField('Email', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ProfileForm(FlaskForm):
    profile_id = StringField('Profile ID (Your profile ID should be the same as your user ID)')
    name = StringField('Full Name', validators=[DataRequired()])
    preference = StringField('Preference', validators=[DataRequired()])
    bio = StringField('Bio', validators=[DataRequired()])
    occupation = StringField('Occupation / Degree', validators=[DataRequired()])
    picture = PasswordField('Profile_Picture', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    submit = SubmitField('Confirm')
    id = StringField('ID number')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class MessageForm(FlaskForm):
    text = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

