import sqlite3
def get_dashboard_stats():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    # Total predictions
    cursor.execute(
        "SELECT COUNT(*) FROM predictions"
    )
    total_predictions = cursor.fetchone()[0]

    # Disease cases
    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE prediction='Disease Detected'
    """)
    disease_cases = cursor.fetchone()[0]

    # Healthy cases
    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE prediction='No Disease Detected'
    """)
    healthy_cases = cursor.fetchone()[0]

    # Average risk
    cursor.execute("""
    SELECT AVG(risk_percentage)
    FROM predictions
    """)
    avg_risk = cursor.fetchone()[0]

    conn.close()

    return {
        "total_predictions": total_predictions,
        "disease_cases": disease_cases,
        "healthy_cases": healthy_cases,
        "avg_risk": round(avg_risk, 2)
        if avg_risk else 0
    }

def save_prediction(country,
                    occupation,
                    risk_percentage,
                    prediction):

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (country, occupation, risk_percentage, prediction)
    VALUES (?, ?, ?, ?)
    """, (
        country,
        occupation,
        risk_percentage,
        prediction
    ))

    conn.commit()
    conn.close()

def get_predictions():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM predictions
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data
def get_risk_stats():

    conn = sqlite3.connect("predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE risk_percentage >= 70
    """)
    high = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE risk_percentage >= 40
    AND risk_percentage < 70
    """)
    moderate = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE risk_percentage < 40
    """)
    low = cursor.fetchone()[0]

    conn.close()

    return {
        "high": high,
        "moderate": moderate,
        "low": low
    }