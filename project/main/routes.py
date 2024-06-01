from flask import render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from project.models.test import User
from project.extensions import db
from flask_login import login_user, login_required, current_user, login_required, logout_user
from project.main import bp
from project.models.basemodel import BaseModel
from project.models.goals import Goal
from project.models.workout import Workout
from project.models.progress import Progress
from project.models.nutrition import Nutrition
from project.models.social import Social



@bp.route('/')
def index():
    return render_template('index.html')
@bp.route('/about')
def about():
    return render_template('about.html')
@bp.route('/services')
def services():
    return render_template('services.html')
@bp.route('/news')
def news():
    return render_template('news.html')
@bp.route('/signup')
def signup():
    return render_template('signup.html')
@bp.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('main.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.login'))
@bp.route('/login')
def login():
    return render_template('login.html')
@bp.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
@bp.route('/profile/fetch_data', methods=['POST'])
@login_required
def fetch_data():
    feature = request.form.get('feature')
    user_id = current_user.id

    if feature == 'goals':
        goals = Goal.query.filter_by(user_id=user_id).all()
        goal_data = [
            {'description': goal.description, 'target_date': goal.target_date.strftime('%Y-%m-%d')}
            for goal in goals
        ]
        return jsonify(goal_data)
    elif feature == 'workouts':
        workouts = Workout.query.filter_by(user_id=user_id).all()
        workout_data = [
            {'date': workout.created_at.strftime('%Y-%m-%d'), 'type': workout.type, 'duration': workout.duration}
            for workout in workouts
        ]
        return jsonify(workout_data)
    elif feature == 'progress':
        progress_records = Progress.query.filter_by(user_id=user_id).all()
        progress_data = [
            {'date': progress.date.strftime('%Y-%m-%d'), 'weight': progress.weight, 'body_fat_percentage': progress.body_fat_percentage}
            for progress in progress_records
        ]
        return jsonify(progress_data)
    elif feature == 'nutrition':
        nutrition_records = Nutrition.query.filter_by(user_id=user_id).all()
        nutrition_data = [
            {'date': nutrition.date.strftime('%Y-%m-%d'), 'calories': nutrition.calories, 'protein': nutrition.protein, 'carbs': nutrition.carbs, 'fats': nutrition.fats}
            for nutrition in nutrition_records
        ]
        return jsonify(nutrition_data)
    else:
        return jsonify({'error': 'Invalid feature'})
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))