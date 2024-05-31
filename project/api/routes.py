from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user  # Import current_user from Flask-Login
from . import utils
from project.api import bp
from project.models.basemodel import BaseModel
from project.models.nutrition import Nutrition
from project.extensions import db
from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

@bp.route('/nutrition', methods=['GET', 'POST'])
def track_nutrition():
    if request.method == 'POST':
        if current_user.is_authenticated:
            food_item = request.form.get('food_item')
            nutrition_data = utils.get_nutrition_data(food_item)
            
            if nutrition_data:
                date_str = nutrition_data.get('date')
                
                if date_str:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    # Set date to current date if not provided
                    date = datetime.now().date()

                # Create a new Nutrition object with dynamic values
                new_nutrition_entry = Nutrition(
                    user_id=current_user.id,
                    date=date,
                    calories=nutrition_data.get('calories', 0),
                    protein=nutrition_data.get('protein', 0),
                    carbs=nutrition_data.get('carbs', 0),
                    fats=nutrition_data.get('fats', 0)
                )

                # Add the new entry to the session
                db.session.add(new_nutrition_entry)

                try:
                    # Attempt to commit the changes to the database
                    db.session.commit()
                except Exception as e:
                    # Handle any database commit exceptions
                    db.session.rollback()
                    return f"Error: {str(e)}"

            return render_template('nutrition_api.html', nutrition_data=nutrition_data)
        else:
            # User is not logged in, redirect to the login page
            return redirect(url_for('main.login'))

    return render_template('nutrition.html')




@bp.route('/download_nutrition_report')
def download_nutrition_report():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(30, height - 40, "Nutrition Report for Fitness")

    # Subtitle
    p.setFont("Helvetica", 12)
    p.drawString(30, height - 60, "General Guidelines and Recommendations")

    # Content
    p.setFont("Helvetica", 10)
    text = """
    1. Protein:
    - Essential for muscle repair and growth.
    - Sources: Lean meats, fish, eggs, dairy, legumes, and nuts.
    - Recommended Intake: 1.2 to 2.2 grams per kilogram of body weight per day.

    2. Carbohydrates:
    - Primary energy source for workouts.
    - Sources: Whole grains, fruits, vegetables, and legumes.
    - Recommended Intake: 3 to 7 grams per kilogram of body weight per day, depending on activity level.

    3. Fats:
    - Important for overall health and hormone production.
    - Sources: Avocado, nuts, seeds, olive oil, and fatty fish.
    - Recommended Intake: 0.5 to 1 gram per kilogram of body weight per day.

    4. Hydration:
    - Crucial for optimal performance and recovery.
    - Drink water throughout the day and during workouts.
    - Aim for at least 8 cups (2 liters) of water per day, more if you're active.

    5. Vitamins and Minerals:
    - Ensure a well-balanced diet with a variety of fruits and vegetables to meet your micronutrient needs.
    - Consider a multivitamin if you have specific deficiencies.

    6. Meal Timing:
    - Eat balanced meals and snacks throughout the day.
    - Post-workout nutrition: Include protein and carbohydrates to aid recovery (e.g., a protein shake with a banana).

    7. Avoid:
    - Excessive processed foods and added sugars.
    - Overeating or undereating; aim for a balanced diet that supports your activity level.

    Remember, individual needs may vary. It's important to consult with a registered dietitian or nutritionist for personalized advice.
    """

    text_lines = text.split("\n")
    y = height - 80
    for line in text_lines:
        p.drawString(30, y, line)
        y -= 12

    # Finish up the PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='nutrition_report.pdf', mimetype='application/pdf')



