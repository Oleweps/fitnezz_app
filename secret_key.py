import secrets
print(secrets.token_hex(16))

#ee04724be1f9299e3dfd9eb7682dbc92
#set SECRET_KEY=ee04724be1f9299e3dfd9eb7682dbc92

@bp.route('/nutrition', methods=['GET', 'POST'])
@login_required
def manage_nutrition():
    if request.method == 'POST':
        date = request.form.get('date')
        calories = request.form.get('calories')
        protein = request.form.get('protein')
        carbs = request.form.get('carbs')
        fats = request.form.get('fats')

        if not date or not calories or not protein or not carbs or not fats:
            flash('All fields are required!', 'danger')
            return redirect(url_for('feature.manage_nutrition'))

        new_nutrition = Nutrition(
            user_id=current_user.id,
            date=date,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats
        )

        db.session.add(new_nutrition)
        db.session.commit()
        flash('Nutrition record has been added!', 'success')
        return redirect(url_for('feature.manage_nutrition'))

    nutrition_records = Nutrition.query.filter_by(user_id=current_user.id).all()
    return render_template('nutrition_api.html', nutrition_records=nutrition_records)


profile.ht
<div class="nutrition-container" onclick="redirectToNutrition()" data-url="{{ url_for('feature.manage_nutrition') }}">
        <h2 class="nutrition-title">Nutrition Tracking</h2>
        <p class="nutrition-description">Track your daily nutrition intake to maintain a balanced diet and achieve your fitness goals. Click here to manage your nutrition.</p>
    </div>