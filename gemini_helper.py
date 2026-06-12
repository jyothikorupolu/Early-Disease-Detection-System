import google.generativeai as genai
import os

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_health_report(patient_data,
                           prediction,
                           risk_percentage):

    try:

        prompt = f"""
        Patient Details:
        {patient_data}

        Prediction:
        {prediction}

        Risk Percentage:
        {risk_percentage}%

        Generate:
        1. Risk Summary
        2. Possible Factors
        3. Recommendations

        Keep it short.
        Consider age is in no.of days
        Cholesterol and gloucose values indicate 1 as normal and 2 as above normal and 3 as well above normal
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI report unavailable: {str(e)}"