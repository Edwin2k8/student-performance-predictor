import streamlit as st
import numpy as np
import pickle
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.pdfgen import canvas

def generate_pdf(study_hours, attendance, sleep_hours, previous_score, prediction):
    file_name = "report.pdf"
    c = canvas.Canvas(file_name)

    c.drawString(100, 750, "Student Performance Report")
    c.drawString(100, 700, f"Study Hours: {study_hours}")
    c.drawString(100, 680, f"Attendance: {attendance}")
    c.drawString(100, 660, f"Sleep Hours: {sleep_hours}")
    c.drawString(100, 640, f"Previous Score: {previous_score}")
    c.drawString(100, 620, f"Predicted Score: {prediction:.2f}")

    c.save()
    return file_name

# ---------------- MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, "..", "models", "model.pkl"), "rb"))



DB_PATH = os.path.join(BASE_DIR, "..", "database", "records.db")
# ---------------- CREATE DATABASE TABLE ----------------
def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_hours REAL,
            attendance REAL,
            sleep_hours REAL,
            previous_score REAL,
            predicted_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Create the table when app starts
create_table()

# ---------------- DB FUNCTION ----------------
def save_to_db(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions 
        (study_hours, attendance, sleep_hours, previous_score, predicted_score)
        VALUES (?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()


# ---------------- GET HISTORY ----------------
def get_history():
    conn = sqlite3.connect(DB_PATH)
    
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY created_at DESC",
        conn
    )
    
    conn.close()
    return df

# ---------------- UI ----------------
st.set_page_config(
    page_title="EduPredict AI",
    page_icon="🎓",
    layout="wide"
)
# ---------------- SIDEBAR ----------------

st.sidebar.title("🎓 EduPredict AI")

page = st.sidebar.radio(
    "Navigation",
    [
    "🏠 Home",
    "📊 Prediction History",
    "📈 Analytics",
    "ℹ️ About Project"
    ]
)

if page == "🏠 Home":

    st.title("🎓 AI Student Performance Predictor")

    st.markdown("""
    ### Welcome to EduPredict AI 🤖

    This intelligent system predicts student performance using Machine Learning.

    ### Features:
    - 🧠 AI-Based Prediction
    - 💾 Prediction History Storage
    - 📄 Automatic PDF Report Generation
    - 📊 Data Analytics Dashboard

    Enter the student details below to get your prediction.
    """)

    # ---------------- INPUT ----------------

    study_hours = st.number_input("Study Hours")
    attendance = st.number_input("Attendance (%)")
    sleep_hours = st.number_input("Sleep Hours")
    previous_score = st.number_input("Previous Score")

    # ---------------- PREDICT ----------------

    if st.button("Predict"):

        input_data = np.array([
            [study_hours, attendance, sleep_hours, previous_score]
        ])

        prediction = model.predict(input_data)[0]

        # Save to database
        save_to_db(
            (
                study_hours,
                attendance,
                sleep_hours,
                previous_score,
                prediction
            )
        )

        st.success(
            f"Predicted Score: {prediction:.2f}"
        )

        # Performance Insights
        if prediction >= 90:
            st.success(
                "🏆 Excellent Performance! Keep maintaining your consistency."
            )

        elif prediction >= 70:
            st.info(
                "👍 Good Performance! You are doing well, but there is still room for improvement."
            )

        else:
            st.warning(
                "⚠️ Needs Improvement. Increase study discipline and improve learning habits."
            )

        # Generate PDF
        pdf_file = generate_pdf(
            study_hours,
            attendance,
            sleep_hours,
            previous_score,
            prediction
        )

        with open(pdf_file, "rb") as f:
            st.download_button(
                "📄 Download Report PDF",
                f,
                file_name="student_report.pdf"
            )

        st.info(
            """
            📊 Explanation:
            - Study Hours impact: High
            - Attendance impact: Medium
            - Previous performance heavily influences result
            """
        )
# ---------------- HISTORY PAGE ----------------

elif page == "📊 Prediction History":

    st.title("📊 Prediction History")

    history = get_history()

    if history.empty:
        st.warning("No prediction records found.")
    else:
        st.success(
            f"Total Predictions Stored: {len(history)}"
        )

        st.dataframe(
            history,
            use_container_width=True
        )

elif page == "📈 Analytics":

    st.title("📈 AI Prediction Analytics")

    history = get_history()

    if history.empty:
        st.warning("No data available for analysis.")

    else:
        st.subheader("Average Prediction Score")

        avg_score = history["predicted_score"].mean()

        st.metric(
            "Average Student Performance",
            f"{avg_score:.2f}"
        )

        st.subheader("Prediction Trend")

        fig, ax = plt.subplots()

        ax.plot(
            history["predicted_score"]
        )

        ax.set_xlabel("Prediction Number")
        ax.set_ylabel("Predicted Score")

        st.pyplot(fig)

# ---------------- ABOUT PAGE ----------------

elif page == "ℹ️ About Project":

    st.title("ℹ️ About EduPredict AI")

    st.markdown("""
    ## 🎓 AI Student Performance Predictor

    EduPredict AI is a machine learning-based web application developed to predict student academic performance using important factors such as:

    - 📚 Study Hours
    - 🏫 Attendance
    - 😴 Sleep Hours
    - 📝 Previous Academic Scores

    ### 🧠 Technologies Used

    - Python
    - Machine Learning (Scikit-learn Linear Regression)
    - Pandas & NumPy
    - Streamlit Web Framework
    - SQLite Database
    - Matplotlib Analytics
    - ReportLab PDF Generation

    ### 💡 Project Features

    ✅ Student performance prediction

    ✅ Prediction history storage

    ✅ Data analytics dashboard

    ✅ Automatic PDF report generation

    ### 👨‍💻 Developer

    Developed by Edwin as a machine learning portfolio project.

    ### 🚀 Future Improvements

    - Larger real-world datasets
    - More advanced machine learning models
    - Cloud deployment
    - User authentication system
    """)