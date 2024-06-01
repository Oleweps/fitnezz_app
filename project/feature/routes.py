from flask import render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from project.models.test import User
from project.extensions import db
from flask_login import login_user, login_required, current_user, logout_user
from project.feature import bp
from datetime import datetime
from project.models.basemodel import BaseModel
from project.models.goals import Goal
from project.models.workout import Workout
from project.models.progress import Progress
from project.models.nutrition import Nutrition
from project.models.social import Social

@bp.route('/goals', methods=['GET', 'POST'])
@login_required
def manage_goals():
    if request.method == 'POST':
        description = request.form.get('description')
        target_date_str = request.form.get('target_date')

        if not description or not target_date_str:
            flash('All fields are required!', 'danger')
            return redirect(url_for('feature.manage_goals'))

        # Convert the string date to a Python date object
        try:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format! Please use YYYY-MM-DD format.', 'danger')
            return redirect(url_for('feature.manage_goals'))

        new_goal = Goal(
            user_id=current_user.id,
            description=description,
            target_date=target_date
        )

        db.session.add(new_goal)
        db.session.commit()
        flash('New goal has been added!', 'success')
        return redirect(url_for('feature.manage_goals'))

    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goal.html', goals=goals)



@bp.route('/progress', methods=['GET', 'POST'])
@login_required
def manage_progress():
    if request.method == 'POST':
        date = request.form.get('date')
        weight = request.form.get('weight')
        body_fat_percentage = request.form.get('body_fat_percentage')

        if not date:
            flash('Date is required!', 'danger')
            return redirect(url_for('feature.manage_progress'))

        new_progress = Progress(
            user_id=current_user.id,
            date=date,
            weight=weight if weight else None,
            body_fat_percentage=body_fat_percentage if body_fat_percentage else None
        )

        db.session.add(new_progress)
        db.session.commit()
        flash('Progress record has been added!', 'success')
        return redirect(url_for('feature.manage_progress'))

    progress_records = Progress.query.filter_by(user_id=current_user.id).all()
    return render_template('progress.html', progress_records=progress_records)

@bp.route('/social', methods=['GET', 'POST'])
@login_required
def manage_social():
    if request.method == 'POST':
        friend_id = request.form.get('friend_id')

        if not friend_id:
            flash('Friend ID is required!', 'danger')
            return redirect(url_for('feature.manage_social'))

        # Check if friend request already exists
        existing_request = Social.query.filter_by(user_id=current_user.id, friend_id=friend_id).first()
        if existing_request:
            flash('Friend request already sent!', 'warning')
            return redirect(url_for('feature.manage_social'))

        new_social = Social(
            user_id=current_user.id,
            friend_id=friend_id,
            status='pending'
        )

        db.session.add(new_social)
        db.session.commit()
        flash('Friend request sent!', 'success')
        return redirect(url_for('feature.manage_social'))

    social_connections = Social.query.filter((Social.user_id == current_user.id) | (Social.friend_id == current_user.id)).all()
    friend_requests = Social.query.filter_by(friend_id=current_user.id, status='pending').all()
    return render_template('social.html', social_connections=social_connections, friend_requests=friend_requests)

@bp.route('/social/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    social_request = Social.query.get_or_404(request_id)
    if social_request.friend_id != current_user.id:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('feature.manage_social'))

    social_request.status = 'accepted'
    db.session.commit()
    flash('Friend request accepted!', 'success')
    return redirect(url_for('feature.manage_social'))

@bp.route('/social/decline/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    social_request = Social.query.get_or_404(request_id)
    if social_request.friend_id != current_user.id:
        flash('You do not have permission to perform this action', 'danger')
        return redirect(url_for('feature.manage_social'))

    social_request.status = 'declined'
    db.session.commit()
    flash('Friend request declined!', 'success')
    return redirect(url_for('feature.manage_social'))

@bp.route('/workouts', methods=['GET', 'POST'])
@login_required
def manage_workouts():
    if request.method == 'POST':
        workout_type = request.form.get('type')
        duration = request.form.get('duration')

        if not workout_type or not duration:
            flash('All fields are required!', 'danger')
            return redirect(url_for('feature.manage_workouts'))

        new_workout = Workout(
            user_id=current_user.id,
            type=workout_type,
            duration=int(duration)
        )

        db.session.add(new_workout)
        db.session.commit()
        flash('New workout has been added!', 'success')
        return redirect(url_for('feature.manage_workouts'))

    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template('workout.html', workouts=workouts)