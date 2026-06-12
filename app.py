import os

from flask import Flask, redirect, render_template, request, session
import numpy as np
import pandas as pd
import sqlite3
from psutil import users
from werkzeug.security import check_password_hash
import joblib
from datetime import datetime
from gemini_helper import generate_health_report
from db_helper import save_prediction
from db_helper import get_predictions
from db_helper import get_dashboard_stats
from db_helper import get_risk_stats

today = datetime.now()

app = Flask(__name__)
app.secret_key=os.getenv("secretkey")

model = joblib.load("model1.pkl")
classifier = model.named_steps['classifier']

feature_names = model.named_steps[
    'preprocessor'
].get_feature_names_out()

importances = classifier.feature_importances_

importance_data = list(
    zip(feature_names, importances)
)

importance_data.sort(
    key=lambda x: x[1],
    reverse=True
)

top_features = importance_data[:5]
feature_mapping = {
    "remainder__age": "Age",
    "remainder__ap_hi": "Systolic Blood Pressure",
    "remainder__ap_lo": "Diastolic Blood Pressure",
    "remainder__weight": "Weight",
    "remainder__height": "Height",
    "remainder__cholesterol": "Cholesterol",
    "remainder__gluc": "Glucose",
    "remainder__gender": "Gender",
    "cat__country_India": "Country (India)",
    "cat__country_Indonesia": "Country (Indonesia)"
}

top_features = [
    (feature_mapping.get(feature, feature), score)
    for feature, score in top_features
]


@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = c.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):

            session['user'] = user[1]  # name
            session['email'] = user[2] # email

            return redirect('/dashboard')

        else:

            return render_template(
                'login.html',
                error="Invalid Email or Password"
            )

    return render_template('login.html')
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')
from werkzeug.security import generate_password_hash
import sqlite3
import re

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

        if not re.match(password_pattern, password):

            return render_template(
                'register.html',
                error="Password must contain uppercase, lowercase, number and special character."
            )

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = c.fetchone()

        if user:

            conn.close()

            return render_template(
                'register.html',
                error="User already exists"
            )

        hashed_password = generate_password_hash(password)

        c.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            'login.html',
            success="Registration Successful! Please Login."
        )

    return render_template('register.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/login')

    features = pd.DataFrame([{
        'country': request.form['country'],
        'active': int(request.form['active']),
        'age': int(request.form['age']),
        'alco': int(request.form['alco']),
        'ap_hi': int(request.form['ap_hi']),
        'ap_lo': int(request.form['ap_lo']),
        'cholesterol': int(request.form['cholesterol']),
        'gender': int(request.form['gender']),
        'gluc': int(request.form['gluc']),
        'height': int(request.form['height']),
        'occupation': request.form['occupation'],
        'smoke': int(request.form['smoke']),
        'weight': float(request.form['weight']),
    }])

    # Prediction
    prediction = model.predict(features)

    probability = model.predict_proba(features)[0][1]

    risk_percentage = round(probability * 100, 2)

    # Result
    if prediction[0] == 1:
        result = "Disease Detected"
    else:
        result = "No Disease Detected"

    # Risk Level
    if risk_percentage >= 70:
        risk_level = "High Risk"
    elif risk_percentage >= 40:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # Patient data for Gemini
    patient_data = {
        "country": request.form['country'],
        "occupation": request.form['occupation'],
        "age": int(request.form['age']),
        "cholesterol": int(request.form['cholesterol']),
        "blood_pressure": f"{request.form['ap_hi']}/{request.form['ap_lo']}",
        "weight": float(request.form['weight'])
    }

    # Generate AI Report
    report = generate_health_report(
        patient_data,
        result,
        risk_percentage
    )
    save_prediction(
    request.form['country'],
    request.form['occupation'],
    risk_percentage,
    result
)

    return render_template(
        "result.html",
        result=result,
        probability=probability,
        risk_percentage=risk_percentage,
        risk_level=risk_level,
        report=report,
        top_features=top_features
    )


@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    predictions = get_predictions()

    return render_template(
        'history.html',
        predictions=predictions
    )
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    stats = get_dashboard_stats()

    return render_template(
        'dashboard.html',
        stats=stats,
        risk_stats=get_risk_stats(),
        disease=stats['disease_cases'],
        healthy=stats['healthy_cases']
    )
if __name__ == "__main__":
    app.run(debug=True)