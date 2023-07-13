from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect
from website.models import User
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

#About Page
@auth.route('/about')
def about():
    return render_template('about.html')

#About2 Page
@auth.route('/about2')
def about2():
    return render_template('about2.html')

#Landing Page
@auth.route('/index')
def index():
    return render_template('index.html')

#Home Page
@auth.route('/home')
def home():
    return render_template('home.html')

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth.route('/welcome')
# @login_required
def welcome():
    return render_template('welcome.html')

# Recommendation page
@auth.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        # Process preference form submission and generate recommendation
        preference1 = request.form['preference1']
        preference2 = request.form['preference2']
        preference3 = request.form['preference3']
        preference4 = request.form['preference4']
        preference5 = request.form['preference5']
        preference6 = request.form['preference6']
        preference7 = request.form['preference7']

        # Generate recommendation based on preferences
        destination = generate_recommendation(preference1, preference2, preference3, preference4, preference5, preference6, preference7)

        # Render the recommendation page with the generated recommendation
        return render_template('result.html', destination=destination)

    # Render the preference form
    return render_template('preferences.html')

def generate_recommendation(preference1, preference2, preference3, preference4, preference5, preference6, preference7):
    dataset = pd.read_csv('preferences.csv')

    # Separate the features (preferences) and the target variable (destinations)
    X = dataset[['preference1', 'preference2', 'preference3', 'preference4', 'preference5', 'preference6', 'preference7']]
    y = dataset['destination']

    model = RandomForestClassifier()
    model.fit(X, y)

    # Prepare the user's preferences as input for prediction
    preferences = [[preference1, preference2, preference3, preference4, preference5, preference6, preference7]]

    # Generate the recommendation using the trained model
    destination = model.predict(preferences)[0]

    return destination

#Admin
@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform admin authentication
        if username == 'admin' and password == 'adminpassword':
            # Redirect to the admin dashboard or editing page
            return redirect('/admin/dashboard')
        else:
            # Handle invalid credentials
            return render_template('admin_login.html', error='Invalid credentials')

    return render_template('admin_login.html', error=None)

@auth.route('/admin/dashboard')
def admin_dashboard():
    # Render the admin dashboard or editing page
    return render_template('admin_dashboard.html')

@auth.route('/admin/edit/palawan', methods=['GET', 'POST'])
def edit_palawan():
    if request.method == 'POST':
        new_content = request.form['content']
        
        return redirect('/admin/dashboard')

    return render_template('edit_palawan.html')

@auth.route('/admin/edit/launion', methods=['GET', 'POST'])
def edit_launion():
    if request.method == 'POST':
        new_content = request.form['content']
        
        return redirect('/admin/dashboard')

    return render_template('edit_launion.html')

@auth.route('/admin/edit/cebu', methods=['GET', 'POST'])
def edit_cebu():
    if request.method == 'POST':
        new_content = request.form['content']
        
        return redirect('/admin/dashboard')

    return render_template('edit_cebu.html')

@auth.route('/admin/edit/baguio', methods=['GET', 'POST'])
def edit_baguio():
    if request.method == 'POST':
        new_content = request.form['content']
        
        return redirect('/admin/dashboard')

    return render_template('edit_baguio.html')

@auth.route('/admin/edit/rizal', methods=['GET', 'POST'])
def edit_rizal():
    if request.method == 'POST':
        new_content = request.form['content']
        
        return redirect('/admin/dashboard')

    return render_template('edit_rizal.html')


#Booking Page
@auth.route('/book')
def book():
    return render_template('book.html')

#Palawan Page
@auth.route('/palawan')
def palawan():
    return render_template('palawan.html')

#Baguio Page
@auth.route('/baguio')
def baguio():
    return render_template('baguio.html')

#Rizal Page
@auth.route('/rizal')
def rizal():
    return render_template('rizal.html')

#La Union Page
@auth.route('/launion')
def launion():
    return render_template('launion.html')

#Cebu Page
@auth.route('/cebu')
def cebu():
    return render_template('cebu.html')



@auth.route('/destinationbtn/<destination>')
def destinationbtn(destination):
    if destination == 'Palawan':
        return redirect('/palawan')
    elif destination == 'Rizal':
        return redirect('/rizal')
    elif destination == 'Baguio':
        return redirect('/baguio')
    else:
        return redirect('/result')