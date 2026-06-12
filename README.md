# 🩺 Early Disease Detection System

An AI-powered healthcare web application that predicts disease risk using Machine Learning and provides intelligent health recommendations. The system helps users assess potential disease risk based on health and lifestyle parameters while offering explainable insights into prediction outcomes.

---

## 🚀 Features

### 🔐 User Authentication

* User Registration
* Secure Login
* Password Hashing
* Session Management
* Logout Functionality

### 🩺 Disease Prediction

* Predicts disease risk using Machine Learning
* Random Forest Classifier
* Risk Percentage Calculation
* Risk Level Classification (Low, Moderate, High)

### 🤖 AI Health Report

* Personalized health recommendations
* AI-generated health insights using Gemini AI

### 🔍 Explainable AI (XAI)

* Displays important factors influencing predictions
* Feature importance visualization
* Improves transparency and trust

### 📊 Analytics Dashboard

* Total Predictions
* Disease Cases
* Healthy Cases
* Average Risk Percentage
* Disease Distribution Charts
* Risk Level Analytics

### 📜 Prediction History

* Stores previous predictions
* View historical records
* SQLite database integration

---

## 🛠 Technologies Used

### Backend

* Python
* Flask
* SQLite

### Machine Learning

* Scikit-Learn
* Random Forest Classifier
* Pandas
* NumPy

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Chart.js

### AI Integration

* Google Gemini AI

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
Early-Disease-Detection-System
│
├── app.py
├── db_helper.py
├── gemini_helper.py
├── train_pipeline.py
├── feature_importance.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   └── history.html
│
├── dataset/
│   └── Data_file - data_file.csv
│
└── scripts/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/jyothikorupolu/Early-Disease-Detection-System.git
cd Early-Disease-Detection-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### Run Application

```bash
flask run
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📈 Machine Learning Model

### Algorithm Used

* Random Forest Classifier

### Dataset

* 70,000 patient records
* Balanced dataset
* Health and lifestyle parameters

### Model Performance

| Metric       | Value          |
| ------------ | -------------- |
| Accuracy     | 72.77%         |
| Algorithm    | Random Forest  |
| Dataset Size | 70,000 Records |

## 🔮 Future Enhancements

* Email Notifications
* PDF Health Reports
* Doctor Recommendation System
* Multi-Disease Prediction
* Cloud Deployment
* Real-time Health Monitoring

---

## 👩‍💻 Author

**Jyothi Korupolu**

Computer Science Undergraduate passionate about Machine Learning, AI Applications, Flask Development, and Intelligent Healthcare Systems.

---

## ⭐ Support

If you found this project useful, please consider giving it a star on GitHub.
