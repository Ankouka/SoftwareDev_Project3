from flask import flash
from app import app, db, load_user
from app.models import User, User_Profile, Message, Soulmate
from app.forms import SignUpForm, SignInForm, ProfileForm, MessageForm
from flask import render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
import json
from flask import current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from datetime import datetime, timedelta
from uuid import uuid4
import random

responses = {
    1: ["hey ", ", dat smile tho... what's the story behind it?"],
    2: ["Heyy, had to say, you're like, hella intriguing, ", ". What's good?"],
    3: ["Hey ", ", ur vibe in that pic is fire! spill the secret sauce?"],
    4: ["heyy ", ", ur profile pic's lit. spill the tea?"],
    5: ["Hey ", ", those eyes tho... what's the story behind 'em?"],
    6: ["Hey ", ", ur vibe in that pic... spill the deets?"],
    7: ["Hey ", ", saw ur pic wanna start a chat?"],
    8: ["Hey ", ", that mystery vibe is intriguing. Tell me more!"],
    9: ["Hey ", ", that smile's contagious. spill the secret sauce?"],
    10: ["Hey ", ", checked ur profile got any dope stories?"]
} #global variable for generated introduction messages

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignInForm()
    errors = []

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):

            login_user(user)
            return redirect(url_for('user_profile'))
        else:
            errors = [field.errors[0] for field in form if field.errors]
            flash('Invalid ID or password. Please try again.', 'error')
    return render_template('signin.html', form=form, errors=errors)


@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            password = form.passwd.data
            confirm_password = form.passwd_confirm.data

            if password == confirm_password:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = User(id=form.id.data, full_name=form.full_name.data, passwd=hashed)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            else:
                flash('Passwords do not match. Please try again.')
                return render_template('signup.html', form=form)

            return redirect(url_for('users_create_profile', form=form, user=current_user))
        except IntegrityError:
            flash('Username already take. Please use a different ID')
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)

@app.route('/users/create profile', methods=['GET', 'POST'])
def users_create_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        try:
             new_profile = User_Profile(profile_id=current_user.id, name=form.name.data, preference=form.preference.data,
                            bio=form.bio.data, occupation=form.occupation.data,
                            picture=form.picture.data, age=form.age.data, sex=form.sex.data)
             db.session.add(new_profile)
             db.session.commit()
             return redirect(url_for('index'))
        except IntegrityError:
            flash('Another user may have the same name as you. Try using a different name')
            return render_template('create_profile.html', form=form)
    else:
        flash('Please fill out all the fields')
        return render_template('create_profile.html', form=form)


@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/users/user_profile', methods=['GET', 'POST'])
def user_profile():
    if current_user.is_authenticated:
        db.session.commit()
        db.session.refresh(current_user)
        user_profile = User_Profile.query.get(current_user.id)
        user = User.query.get(current_user.id)
        soulmates = user.soulmates
        
        return render_template('user_profile.html', user=current_user, user_profile=user_profile, profiles=db.session.query(User_Profile), soulmates=soulmates)
    else:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('users_signin'))

@login_required
@app.route('/users/soulmates')
def potential_partners():
    if current_user.is_authenticated:
        user_soulmate_ids = [soulmate.id for soulmate in current_user.soulmates]
        user_profile = User_Profile.query.get(current_user.id)

        if user_profile.preference == 'Male':
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids), Soulmate.gender == 'Male').all()
        elif user_profile.preference == 'Female':
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids), Soulmate.gender == 'Female').all()
        else:
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids)).all()
    else:
        soulmates = Soulmate.query.all()

    return render_template('soulmates_profile.html', soulmates = soulmates)

@login_required
@app.route('/users/edit profile', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()

    #Searches a user's profile by their profile id
    user_profile = User_Profile.query.get(current_user.id)
    if form.validate_on_submit():
        try:
            print("BEFORE: User Profile Name", user_profile.name )
        # Update the user profile with the form data
            user_profile.name = form.name.data
            user_profile.preference = form.preference.data
            user_profile.occupation = form.occupation.data
            user_profile.age = form.age.data
            user_profile.sex = form.sex.data
            user_profile.bio = form.bio.data
            user_profile.picture = form.picture.data
            print("AFTER: User Profile Name", user_profile.name)
        # Save the changes to the database
            db.session.commit()
            return redirect(url_for('user_profile', user=user_profile))

        except Exception as e:
            print("Error updating profile: ", e)
            flash('Error updating profile. Please try again.')
            return redirect(url_for('user_profile', user=user_profile))
    return render_template('edit_profile.html', user_profile=user_profile, form=form)


@app.route('/save_soulmate_info', methods=['POST'])
def save_soulmate_info():
    soulmate_info = request.json

    # Ensure that soulmate_info is a dictionary
    if not isinstance(soulmate_info, dict):
        return jsonify({'success': False, 'error': 'Invalid soulmate_info format'}), 400

    # Here you can store the soulmate_info in the session or in a database
    # For simplicity, let's store it in the session
    session['soulmate_info'] = soulmate_info

    return jsonify({'success': True})


@app.route('/add_soulmate/', defaults={'id' : 'NOBODY'}, methods=['GET', 'POST'])
@app.route('/add_soulmate/<id>', methods=['POST', 'GET'],)
@login_required
def add_soulmate(id):

    user = User.query.get(current_user.id)
    soulmate = Soulmate.query.get(id)

    user.soulmates.append(soulmate)

    response = responses[random.randint(1,10)][0] + str((User_Profile.query.get(current_user.id)).name) + responses[random.randint(1,10)][1]
    message = Message(message_id=str(uuid4()), user_id=id, recipient=current_user.id,
                      text=response, time=datetime.now())
    db.session.add(message)
    db.session.commit()

    if current_user.is_authenticated:
        user_soulmate_ids = [soulmate.id for soulmate in current_user.soulmates]
        user_profile = User_Profile.query.get(current_user.id)

        if user_profile.preference == 'Male':
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids), Soulmate.gender == 'Male').all()
        elif user_profile.preference == 'Female':
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids), Soulmate.gender == 'Female').all()
        else:
            soulmates = Soulmate.query.filter(Soulmate.id.notin_(user_soulmate_ids)).all()
    else:
        soulmates = Soulmate.query.all()

    return render_template('soulmates_profile.html', soulmates = soulmates)


@app.route('/view_matches')
def view_matches():
    matches = current_user.soulmates
    return render_template('view_matches.html', matches = matches)


@app.route('/chat/', defaults={'recipient' : 'NOBODY'}, methods=['GET', 'POST'])
@app.route('/chat/<recipient>', methods=['GET', 'POST'])
def chat(recipient):
    if recipient != "NOBODY":
        soulmate = Soulmate.query.get(recipient)

        form = MessageForm()
        if form.validate_on_submit():
            try:
                message = Message(message_id=str(uuid4()), user_id=current_user.id, recipient=recipient,
                                       text=form.text.data, time=datetime.now())
                db.session.add(message)
                db.session.commit()
            except IntegrityError:
                flash('An error has occured. Please try again')
                return redirect(url_for('user_profile', user=user_profile))
        messages = Message.query.order_by(Message.time).filter(
            ((Message.user_id == current_user.id) | (Message.user_id == recipient)) & (
                    (Message.recipient == current_user.id) | (Message.recipient == recipient))).all()
        return render_template('chat.html', soulmate=soulmate, user=User_Profile.query.get(current_user.id),
                               messages=messages, form=form, current_user=current_user.id)
    flash('An error has occured. Please try again')
    return redirect(url_for('user_profile', user=user_profile))

